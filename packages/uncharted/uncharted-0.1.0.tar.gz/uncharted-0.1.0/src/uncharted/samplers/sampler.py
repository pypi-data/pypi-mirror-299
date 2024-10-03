"""Base classes for samplers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Generator, Sequence
from typing import TYPE_CHECKING

import numpy as np

from ..parameters import ParameterSpace

if TYPE_CHECKING:
    from ..explorer import Explorer


class StopExploration(Exception):
    """Raised if competion conditions are met before the maximum number of trials."""

    pass


class Sampler(ABC):
    """Base class for samplers."""

    def __init__(self, deterministic: bool = False):
        """Initialize the sampler."""
        self._explorer = None
        self.deterministic = deterministic

    def assign(self, explorer: Explorer) -> Sampler:
        """Assign an explorer to the sampler."""
        self._explorer = explorer
        return self

    def _is_duplicate(self, x: np.ndarray) -> bool | None:
        """Check if the current sample `x` is a duplicate."""
        xs = self._explorer.results.x
        if self.deterministic:
            return np.isclose(xs, x).all(axis=1).any()

    @abstractmethod
    def sample(self, params: ParameterSpace) -> np.ndarray:
        """Sample a single point from the current parameter space."""
        pass

    def sample_batch(self, params: ParameterSpace, n: int) -> np.ndarray:
        """Sample multiple points from the current parameter space at once."""
        return np.array([self.sample(params) for _ in range(n)])

    def update(self, x: np.ndarray, y: np.ndarray) -> None:
        """Update the sampler with new data."""
        raise NotImplementedError("This sampler does not support updating.")


class BatchSampler(Sampler, ABC):
    """Base class for samplers that produce a batch of samples."""

    def __init__(self, **kwargs):
        """Initialize the sampler."""
        super().__init__(**kwargs)
        self._params = None
        self._samples = None

    @abstractmethod
    def _get_samples(self) -> Sequence:
        """Get a batch of samples."""
        pass

    def _post_batch(self) -> None:
        """Callback called once a batch has been exhausted."""
        pass

    def _sample_generator(self) -> Generator[np.ndarray, None, None]:
        """Generate samples from a batch."""
        # continously generate batches of samples
        while True:
            samples = self._get_samples()
            yield from samples
            self._post_batch()

    def _ensure_samples(self, params: ParameterSpace) -> Generator[np.ndarray, None, None]:
        """Ensure the sampler is ready to generate samples."""
        # assign the current parameter space to the sampler in case the samples batch
        # needs to be regenerated
        self._params = params
        # start the generator if it hasn't been started yet
        if self._samples is None:
            self._samples = self._sample_generator()
        return self._samples

    def sample(self, params: ParameterSpace) -> np.ndarray:
        """Sample a single point from the current parameter space."""
        samples = self._ensure_samples(params)
        return np.asarray(next(samples))

    def sample_batch(self, params: ParameterSpace, n: int) -> np.ndarray:
        """Sample multiple points from the current parameter space at once."""
        samples = self._ensure_samples(params)
        batch = [next(samples) for _ in range(n)]
        return np.array(batch)
