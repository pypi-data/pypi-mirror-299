"""Classes for exploring a function's parameter space."""

import warnings
from collections.abc import Callable, Collection, Sequence
from dataclasses import dataclass

import numpy as np
from loguru import logger

from .criteria import Criterion
from .parameters import Parameter, ParameterSpace
from .samplers.sampler import Sampler, StopExploration


@dataclass
class Results:
    """Stores the results of an exploration."""

    x: np.ndarray
    y: np.ndarray

    @staticmethod
    def _format_xy(x: np.ndarray | Sequence, y: np.ndarray | Sequence) -> tuple[np.ndarray, np.ndarray]:
        """Ensure that x and y are arrays of shape (n_samples, n_features)."""
        x = np.atleast_1d(x)
        y = np.atleast_1d(y)
        _preformat = (x.shape, y.shape)
        if x.ndim == 1 and y.size == 1:  # scalar y, vector x -> single sample
            x = np.expand_dims(x, 0)  # expand to single sample
        elif x.ndim == 1 and len(x) == len(y):  # vector x, vector y -> assume multiple samples
            x = np.expand_dims(x, -1)  # expand x to single feature
        _postformat = (x.shape, y.shape)
        logger.debug(f"Pre-formatted data shapes: {_preformat}, post-formatted data shapes: {_postformat}")
        assert (
            y.shape[0] == x.shape[0]
        ), f"x and y should have the same number of samples ({y.shape} != {x.shape} along axis=0)"
        return x, y

    def __post_init__(self):
        """Initialize the results."""
        self.x, self.y = self._format_xy(self.x, self.y)

    def __len__(self) -> int:
        """Return the number of data points in the results."""
        return len(self.y)

    def __iter__(self):
        """Iterate over the data points in the results."""
        return zip(self.x, self.y)

    def append(self, x: np.ndarray | Sequence, y: np.ndarray | Sequence) -> None:
        """Append new data to the results."""
        x, y = self._format_xy(x, y)
        logger.info(f"Appending data with shapes ({x.shape}, {y.shape}) to dataset ({self.x.shape}, {self.y.shape})")
        self.x = np.concatenate([self.x, x]) if self.x.size else x
        self.y = np.concatenate([self.y, y]) if self.y.size else y


class Explorer:
    """Explores a parameter space."""

    def __init__(
        self,
        params: Sequence[Parameter],
        sampler: Sampler,
        criteria: Collection[Callable[[Results], bool] | Criterion] | None = None,
        all_criteria: bool = False,
    ):
        """Initialize the explorer.

        Parameters:
            params: The parameters to explore.
            sampler: The sampler to use for exploring the parameter space.
            criteria: The termination criteria for the exploration.
            all_criteria: Whether all criteria must be met for the exploration to terminate.
        """
        self._params = ParameterSpace(params)
        self.sampler = sampler.assign(self)
        self.results = Results([], [])
        self.criteria = criteria or []
        self.all_criteria = all_criteria
        self._finished = False
        sampler_has_termination = hasattr(self.sampler, "has_termination") and self.sampler.has_termination
        if len(self.criteria) == 0 and not sampler_has_termination:
            warnings.warn("No termination criteria provided; exploration may run indefinitely")

    @property
    def is_finished(self) -> bool:
        """Check if the exploration is finished."""
        return self._finished

    def ask(self, n: int = 1) -> np.ndarray:
        """Request a number of parameter samples."""
        if n > 1:
            return self.sampler.sample_batch(self._params, n)
        else:
            return self.sampler.sample(self._params)

    def tell(self, x: np.ndarray, y: np.ndarray, n: int = 1) -> None:
        """Update the sampler with new data.

        `n` should be set to the number of results if more than one is being provided.
        """
        if n > 1 and x.ndim == 1:  # multiple samples of scalar x
            x = np.expand_dims(x, -1)  # expand x to single feature
        self.results.append(x, y)
        try:
            self.sampler.update(self.results.x, self.results.y)
        except NotImplementedError:
            pass

    def should_terminate(self) -> bool:
        """Check if the exploration should terminate."""
        logic = all if self.all_criteria else any
        return logic(criterion(self.results) for criterion in self.criteria)

    def explore(self, f: Callable, batch_size: int = 1) -> Results:
        """Explore the parameter space.

        Parameters:
            f: The function to explore.
            batch_size: The number of samples to take at once.

        Returns:
            The results of the exploration.
        """
        # explore the parameter space until the termination criteria are met
        while not self.is_finished:
            try:
                x = self.ask(batch_size)  # request a number of points to sample
                y = f(x)
                self.tell(x, y, batch_size)
            except StopExploration as e:
                logger.info(f"Stopping exploration: {e}")
                break
            # check termination criteria to determine if exploration should continue
            if self.should_terminate():
                logger.info("Exploration terminated")
                break
        return self.results
