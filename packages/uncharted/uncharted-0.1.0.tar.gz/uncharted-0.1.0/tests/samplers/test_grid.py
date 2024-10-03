"""Test the uncharted.samplers.grid module."""

from uncharted.samplers.grid import GridSampler
from uncharted.parameters import Parameter, ParameterSpace
import numpy as np
import pytest
import logging

logger = logging.getLogger(__name__)


@pytest.fixture
def params():
    return ParameterSpace([Parameter(-1, 1, step=0.2), Parameter(0, 2, step=0.2)])


class TestGridSampler:
    @pytest.fixture
    def sampler(self):
        return GridSampler()

    def test_sample(self, sampler, params):
        n = 100
        samples = np.stack([sampler.sample(params) for _ in range(n)])
        assert samples.shape == (n, 2)
        assert all((samples[:, 0] >= -1) & (samples[:, 0] <= 1))
        assert all((samples[:, 1] >= 0) & (samples[:, 1] <= 2))

    def test_sample_batch(self, sampler, params):
        samples = sampler.sample_batch(params, 100)
        assert samples.shape == (100, 2)
        assert all((samples[:, 0] >= -1) & (samples[:, 0] <= 1))
        assert all((samples[:, 1] >= 0) & (samples[:, 1] <= 2))

    def test_shuffle(self, params):
        sampler = GridSampler(shuffle=False)
        ordered = list(sampler._ensure_gridpoints(params))
        sampler = GridSampler(shuffle=True)
        shuffled = list(sampler._ensure_gridpoints(params))
        assert not np.allclose(ordered, shuffled)
        assert set(map(tuple, ordered)) == set(map(tuple, shuffled))
