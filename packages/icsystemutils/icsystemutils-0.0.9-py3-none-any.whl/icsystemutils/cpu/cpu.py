"""
This module has elements of a CPU
"""

from pydantic import BaseModel


class ProcessorThread(BaseModel):
    """Class representing a logical thread on a processor core"""

    identifier: int


class ProcessorCore(BaseModel):
    """Class representing a core on a processor"""

    identifier: int
    threads: list[ProcessorThread]

    @property
    def num_threads(self) -> int:
        return len(self.threads)


class PhysicalProcessor(BaseModel):
    """Class representing a real (physical) processor"""

    identifier: int
    cores: list[ProcessorCore]
    core_count: int = 0
    model: str = ""
    cache_size: int = 0
    sibling: int = 1

    @property
    def num_cores(self) -> int:
        return len(self.cores)
