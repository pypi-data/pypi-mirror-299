"""Sampler that samples from a pre-defined grid of points in the parameter space."""

from collections.abc import Generator
from functools import reduce
from itertools import islice, product

import numpy as np
from loguru import logger

from ..parameters import ParameterSpace
from .sampler import Sampler, StopExploration


class GridSampler(Sampler):
    """Sample from a grid of parameter values."""

    has_termination: bool = True

    def __init__(self, shuffle: bool = False, **kwargs):
        """Initialize the sampler."""
        self._shuffle = shuffle
        self._gridpoints = None
        self.size = None
        super().__init__(**kwargs)

    def _ensure_gridpoints(self, params: ParameterSpace) -> Generator[np.ndarray, None, None]:
        """Ensure the grid points are generated."""
        if self._gridpoints is None:
            for i, parameter in enumerate(params.parameters):
                name = parameter.name if parameter.name is not None else i
                assert parameter.step is not None, f"Parameter {name} missing a step size"
            arrays = params.get_arrays()
            self.size = reduce(lambda x, y: x * y, map(len, arrays))
            logger.debug(f"Generating {self.size} samples")
            self._gridpoints = product(*arrays)
            if self._shuffle:
                rng = np.random.default_rng()
                shuffled = rng.permutation(list(self._gridpoints))
                self._gridpoints = iter(shuffled)
        return self._gridpoints

    def sample(self, params: ParameterSpace) -> np.ndarray:
        """Sample a single point from the current parameter space."""
        grid = self._ensure_gridpoints(params)
        try:
            return np.asarray(next(grid))
        except StopIteration:
            raise StopExploration("Exhausted grid points")

    def sample_batch(self, params: ParameterSpace, n: int) -> np.ndarray:
        """Sample multiple points from the current parameter space at once."""
        grid = self._ensure_gridpoints(params)
        batch = list(islice(grid, n))
        if len(batch) == 0:
            raise StopExploration("Exhausted grid points")
        return np.array(batch)


class CornerSampler(GridSampler):
    """Sample the corners of the parameter space."""

    def __init__(self, mids: bool = True, **kwargs):
        """Initialize the sampler."""
        self.mids = mids
        super().__init__(**kwargs)

    def _ensure_gridpoints(self, params: ParameterSpace) -> Generator[np.ndarray, None, None]:
        """Ensure the grid points are generated."""
        if self._gridpoints is None:
            endpoints = [
                (p.min_value, p.nominal, p.max_value) if self.mids else (p.min_value, p.max_value) for p in params
            ]
            self.size = 2 ** len(params)
            logger.debug(f"Generating {self.size} samples")
            self._gridpoints = product(*endpoints)
        return self._gridpoints
