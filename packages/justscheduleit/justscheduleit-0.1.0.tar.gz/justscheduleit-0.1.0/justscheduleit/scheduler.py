from __future__ import annotations

import dataclasses as dc
import inspect
import logging
from collections.abc import AsyncGenerator, AsyncIterator, Iterator, Collection
from contextlib import asynccontextmanager, contextmanager
from functools import partial
from typing import (
    TYPE_CHECKING,
    Any,
    Awaitable,
    Callable,
    Generic,
    Protocol,
    TypeVar,
    Union,
    cast,
    final, overload,
)

import anyio
from anyio import (
    CancelScope,
    create_memory_object_stream,
    create_task_group,
    get_cancelled_exc_class,
    to_thread,
)
from anyio.from_thread import BlockingPortal
from anyio.streams.memory import MemoryObjectReceiveStream, MemoryObjectSendStream
from typing_extensions import ParamSpec, Self

from justscheduleit._utils import NULL_CM, choose_anyio_backend, observe_event, task_full_name, EventView
from justscheduleit.hosting import Host, HostLifetime, ServiceLifetime

# Optional dependencies
if TYPE_CHECKING:
    # noinspection PyPackageRequirements
    from opentelemetry.trace import Tracer, TracerProvider

T = TypeVar("T")
TriggerEventT = TypeVar("TriggerEventT")
TaskT = Union[Callable[..., Awaitable[T]], Callable[..., T]]
P = ParamSpec("P")

__all__ = [
    "Scheduler",
    "SchedulerLifetime",
    "ScheduledTask",
    "TaskExecutionFlow",
    "TaskT",
    "Trigger",
    "TriggerFactory",
    "arun",
    "run",
    "aserve",
    "serve",
]

logger = logging.getLogger(__name__)


class TaskExecutionFlow(Protocol[T, TriggerEventT]):
    @property
    def task(self) -> ScheduledTask[T, TriggerEventT]: ...

    def subscribe(self) -> MemoryObjectReceiveStream[T]: ...


@dc.dataclass(slots=True)
class _TaskExecutionFlow(Generic[T, TriggerEventT]):
    task: ScheduledTask[T, TriggerEventT]
    results: MemoryObjectSendStream[T]
    _results_reader: MemoryObjectReceiveStream[T]

    def __init__(self, task: ScheduledTask[T, Any]):
        self.task = task
        self.results, self._results_reader = create_memory_object_stream[T]()

    @property
    def is_observed(self) -> bool:
        return self._results_reader.statistics().open_receive_streams > 1

    def subscribe(self) -> MemoryObjectReceiveStream[T]:
        return self._results_reader.clone()


class _TaskExecution(Generic[T, TriggerEventT]):
    task: ScheduledTask[T, TriggerEventT]
    exec_flow: _TaskExecutionFlow[T, TriggerEventT]
    trigger: AsyncGenerator[TriggerEventT, T]

    _async_target: Callable[..., Awaitable[T]]
    """
    The target function, maybe wrapped (if the task's target is a sync function).
    """

    _scope: CancelScope | None
    """
    Graceful shutdown scope.

    1. Stop listening for new trigger events.
    2. Wait for the current task function call to complete (a task function with a CancelScope parameter can
       optimize the shutdown process internally).
    """

    _tracer: Tracer | None

    def __init__(self, exec_flow: _TaskExecutionFlow[T, TriggerEventT], scheduler_lifetime: SchedulerLifetime):
        task = exec_flow.task
        self.task = task
        self.exec_flow = exec_flow
        self.trigger = task.trigger(scheduler_lifetime)

        t = task.target
        self._async_target = cast(
            Callable[..., Awaitable[T]], t if inspect.iscoroutinefunction(t) else partial(to_thread.run_sync, t)
        )

        self._scope = None
        self._tracer = scheduler_lifetime.scheduler._tracer  # noqa

    @property
    def has_started(self) -> bool:
        return self._scope is not None

    async def __call__(self, service_lifetime: ServiceLifetime) -> None:
        if self.has_started:
            raise RuntimeError("Task already started")

        self._scope = service_lifetime.graceful_shutdown_scope = shutdown_scope = CancelScope()
        service_lifetime.set_started()

        # Iterate manually, as we want to use the shutdown scope only for the waiting part

        trigger = self.trigger
        # Initialize the event stream, as per the (async) generator protocol
        move_next = trigger.asend(None)  # type: ignore
        async with self.exec_flow.results:
            try:
                while True:
                    with shutdown_scope:
                        event = await move_next
                    if shutdown_scope.cancel_called:
                        break
                    try:
                        result = await self._execute_task(event)
                        move_next = trigger.asend(result)
                    except get_cancelled_exc_class():  # noqa
                        raise  # Propagate cancellation
                    except Exception as exc:  # noqa
                        move_next = trigger.athrow(exc)
            except StopAsyncIteration:  # As per https://docs.python.org/3/reference/expressions.html#agen.asend
                pass  # Event stream has been exhausted
            finally:
                await trigger.aclose()

    async def _execute_task(self, event: Any) -> T:
        root_span = NULL_CM
        if self._tracer:
            # TODO Inside the thread, for sync tasks?..
            root_span = self._tracer.start_as_current_span(self.task.name)  # type: ignore
        with root_span:
            if self.task.event_aware:
                result = await self._async_target(event)
            else:
                result = await self._async_target()
        if self.exec_flow.is_observed:
            await self.exec_flow.results.send(result)
        return result


@final
@dc.dataclass(frozen=True, slots=True)
class ScheduledTask(Generic[T, TriggerEventT]):
    name: str
    target: TaskT[T]
    trigger: TriggerFactory[TriggerEventT, T]
    _: dc.KW_ONLY
    event_aware: bool = False
    """
    Whether the target function accepts an event parameter.

    By default, detected based on the target's signature (number of parameters). Can be overridden (in case the
    autodetect value is incorrect).
    """

    def __repr__(self):
        return f"{self.__class__.__name__}({self.name!r}, {self.trigger!r})"

    @classmethod
    def create(cls, target: TaskT[T], trigger: TriggerFactory, /, *, name: str | None = None) -> Self:
        return cls(name or task_full_name(target), target, trigger,
                   event_aware=len(inspect.signature(target).parameters) > 0)


class SchedulerLifetime:
    """
    Execution manager, for _outside_ control of the scheduler.
    """

    def __init__(self,
                 scheduler: Scheduler, exec_flows: Collection[TaskExecutionFlow],
                 service_lifetime: ServiceLifetime):
        self.scheduler = scheduler
        self._tasks = {exec_flow.task: exec_flow for exec_flow in exec_flows}
        self._service_lifetime = service_lifetime

    def __repr__(self):
        return f"<{self.__class__.__name__} for {self.scheduler!r}>"

    @property
    def started(self) -> EventView:
        return self._service_lifetime.started

    @property
    def shutting_down(self) -> EventView:
        return self._service_lifetime.shutting_down

    @property
    def stopped(self) -> EventView:
        return self._service_lifetime.stopped

    @property
    def host_portal(self) -> BlockingPortal:
        return self._service_lifetime.host_portal

    @overload
    def find_exec_for(self, task: TaskT[T]) -> TaskExecutionFlow[T, Any] | None:
        ...

    @overload
    def find_exec_for(self, task: ScheduledTask[T, TriggerEventT]) -> TaskExecutionFlow[T, TriggerEventT] | None:
        ...

    def find_exec_for(self, task: TaskT[T] | ScheduledTask[T, Any]) -> TaskExecutionFlow[T, Any] | None:
        if isinstance(task, ScheduledTask):
            return self._tasks.get(task)

        for task_exec in self._tasks.values():
            if task_exec.task.target == task:
                return task_exec

        return None

    def shutdown(self) -> None:
        self._service_lifetime.shutdown()


Trigger = AsyncGenerator[TriggerEventT, T]
TriggerFactory = Callable[[SchedulerLifetime], AsyncGenerator[TriggerEventT, T]]


@final
class Scheduler:
    name: str
    tasks: list[ScheduledTask]

    _lifetime: SchedulerLifetime | None
    _tracer: Tracer | None

    __slots__ = ("name", "tasks", "_lifetime", "_tracer")

    def __init__(self, name: str | None = None):
        self.name = name or "default_scheduler"
        self.tasks = []
        self._lifetime = None
        try:  # By default, try to enable OpenTelemetry instrumentation
            self.instrument()
        except RuntimeError:
            self._tracer = None

    def instrument(self, tracer_provider: TracerProvider | None = None):
        if self._is_running:
            raise RuntimeError("Cannot change instrumentation setting on a running scheduler")
        try:
            # noinspection PyPackageRequirements
            from opentelemetry.trace import get_tracer_provider

            from justscheduleit import __version__

            tracer_provider = tracer_provider or get_tracer_provider()
            self._tracer = tracer_provider.get_tracer(__name__, __version__)
        except ImportError:
            raise RuntimeError("OpenTelemetry package is not available") from None

    def uninstrument(self):
        if self._is_running:
            raise RuntimeError("Cannot change instrumentation setting on a running scheduler")
        self._tracer = None

    @property
    def _is_running(self) -> bool:
        return self._lifetime is not None

    @property
    def lifetime(self) -> SchedulerLifetime:
        if self._lifetime:
            return self._lifetime
        raise RuntimeError("Scheduler not running")

    def __repr__(self):
        return f"<{self.__class__.__name__} with {len(self.tasks)} tasks>"

    def add_task(
        self,
        func: TaskT[T],
        trigger: TriggerFactory[TriggerEventT, T],
        *,
        name: str | None = None,
    ) -> ScheduledTask[T, TriggerEventT]:
        task = ScheduledTask.create(func, trigger, name=name)
        self.tasks.append(task)
        return task

    def task(self, trigger: TriggerFactory, *, name: str | None = None) -> Callable[[Callable[P, T]], Callable[P, T]]:
        """
        Decorator to register a new task.
        """

        def decorator(func: Callable[P, T]) -> Callable[P, T]:
            self.add_task(func, trigger, name=name)
            return func

        return decorator

    async def __call__(self, service_lifetime: ServiceLifetime) -> None:
        """
        Run as a hosted service.
        """
        logger.debug("Starting tasks host...")
        tasks = [_TaskExecutionFlow(task) for task in self.tasks]
        self._lifetime = scheduler_lifetime = SchedulerLifetime(self, tasks, service_lifetime)
        try:
            tasks_host = Host(f"{self.name}_tasks_host")
            for exec_flow in tasks:
                tasks_host.add_service(_TaskExecution(exec_flow, scheduler_lifetime), name=exec_flow.task.name)
            tasks_host_lifetime: HostLifetime
            async with tasks_host.aserve(service_lifetime.host_portal) as tasks_host_lifetime:
                async with create_task_group() as tg:
                    # Service supervisor will cancel this (inner) scope on shutdown, not the whole task. So the context
                    # manager will exit normally, shutting down the host.
                    service_lifetime.graceful_shutdown_scope = tg.cancel_scope
                    # Host lifetime observers, to update the service state
                    observe_event(tg, tasks_host_lifetime.started, lambda: service_lifetime.set_started())
                    observe_event(tg, tasks_host_lifetime.shutting_down, lambda: service_lifetime.shutdown())
                    observe_event(tg, tasks_host_lifetime.stopped, lambda: service_lifetime.shutdown())
        finally:
            self._lifetime = None


def _host(scheduler: Scheduler):
    host = Host(f"{scheduler.name}_host")
    host.add_service(scheduler, name="scheduler")
    return host


@asynccontextmanager
async def aserve(scheduler: Scheduler) -> AsyncIterator[HostLifetime]:
    async with _host(scheduler).aserve() as host_lifetime:
        yield host_lifetime


@contextmanager
def serve(scheduler: Scheduler) -> Iterator[HostLifetime]:
    with _host(scheduler).serve() as host_lifetime:
        yield host_lifetime


async def arun(scheduler: Scheduler):
    from justscheduleit import hosting

    await hosting.arun(_host(scheduler))


def run(scheduler: Scheduler):
    anyio.run(arun, scheduler, **choose_anyio_backend())
