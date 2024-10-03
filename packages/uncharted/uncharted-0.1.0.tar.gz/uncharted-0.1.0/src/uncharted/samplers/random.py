"""Random samplers."""

from math import ceil, log2

import numpy as np
from loguru import logger
from scipy.stats import qmc

from ..parameters import ParameterSpace
from .sampler import BatchSampler, Sampler


class RandomSampler(Sampler):
    """Uniform random sampler."""

    def __init__(self, seed=None, **kwargs):
        """Initialize the sampler."""
        self._rng = np.random.default_rng(seed)
        super().__init__(**kwargs)

    def sample(self, params: ParameterSpace) -> np.ndarray:
        """Sample a single point from the current parameter space."""
        return self._rng.uniform(*params.limits)

    def sample_batch(self, params: ParameterSpace, n: int) -> np.ndarray:
        """Sample multiple points from the current parameter space at once."""
        return self._rng.uniform(*params.limits, size=(n, len(params)))


class QMCSampler(BatchSampler):
    """Quasi-Monte-Carlo sampler.

    Samples are generated using the Sobol sequence from `scipy.stats.qmc` to provide a
    uniform distribution of points. A sequence is generated where the size is the next
    power of 2 greater than the maximum number of samples requested. Once the sequence
    is exhausted it will regenerate.
    """

    def __init__(self, max_samples: int = 1024, seed: int | None = None, **kwargs):
        """Initialize the sampler.

        Parameters:
            max_samples: The maximum number of samples to generate.
            seed: Seed for the Sobol sequence.
        """
        self._max_samples = max_samples
        self._seed = seed
        super().__init__(**kwargs)

    def _get_samples(self) -> np.ndarray:
        """Generate a batch of samples."""
        logger.debug(f"Generating {self._max_samples} samples")
        sampler = qmc.Sobol(d=len(self._params), seed=self._seed)
        m = ceil(log2(self._max_samples))
        samples = sampler.random_base2(m)
        scaled = qmc.scale(samples, *self._params.limits)
        return scaled

    def _post_batch(self) -> None:
        self._seed += 1  # increment the seed to generate a new sequence in the next batch
