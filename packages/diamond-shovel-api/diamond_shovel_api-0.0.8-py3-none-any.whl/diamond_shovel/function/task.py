from enum import Enum
from typing import Callable, Coroutine, Any


class WorkerScope(Enum):
    INFO_COLLECTION = "info_collection"
    VULNERABILITY_SCAN = "vulnerability_scan"
    REPORT_GENERATION = "report_generation"


TaskContext = {}


class WorkerPool:
    def register_worker(self, worker: Callable[[TaskContext], Coroutine[Any, Any, Any]]):
        ...

pools: dict[str, WorkerPool] = {}
