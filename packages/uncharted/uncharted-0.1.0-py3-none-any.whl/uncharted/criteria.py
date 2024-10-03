"""Termination critera."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from loguru import logger

if TYPE_CHECKING:
    from .explorer import Results


class Criterion(ABC):
    """Base class for termination criteria."""

    @abstractmethod
    def __call__(self, results: "Results") -> bool:
        """Check if the termination criteria are met."""
        pass


class MaxSamples(Criterion):
    """Termination criterion based on the number of samples taken."""

    def __init__(self, n: int):
        """Initialize the criterion."""
        self.n = n

    def __call__(self, results: "Results") -> bool:
        """Check if the termination criteria are met."""
        res = len(results) >= self.n
        if res:
            logger.info(f"Termination criterion met: {len(results)} samples >= {self.n}")
        return res
