"""Test the uncharted.samplers.random module."""

from uncharted.samplers.random import RandomSampler, QMCSampler
from uncharted.parameters import Parameter, ParameterSpace
import numpy as np
import pytest
import logging


@pytest.fixture
def params():
    return ParameterSpace([Parameter(-1, 1), Parameter(0, 2)])


class TestRandomSampler:
    @pytest.fixture
    def sampler(self):
        return RandomSampler(seed=0)

    def test_sample(self, sampler, params):
        sample = sampler.sample(params)
        assert sample.shape == (2,)
        samples = np.stack([sampler.sample(params) for _ in range(100)])
        assert samples.shape == (100, 2)
        assert all((samples[:, 0] >= -1) & (samples[:, 0] <= 1))
        assert all((samples[:, 1] >= 0) & (samples[:, 1] <= 2))

    def test_sample_batch(self, sampler, params):
        samples = sampler.sample_batch(params, 100)
        assert samples.shape == (100, 2)
        assert all((samples[:, 0] >= -1) & (samples[:, 0] <= 1))
        assert all((samples[:, 1] >= 0) & (samples[:, 1] <= 2))


class TestQMCSampler:
    @pytest.fixture
    def sampler(self):
        return QMCSampler(max_samples=100, seed=0)

    def test_sample(self, sampler, params):
        sample = sampler.sample(params)
        assert sample.shape == (2,)
        samples = np.stack([sampler.sample(params) for _ in range(100)])
        assert samples.shape == (100, 2)
        assert all((samples[:, 0] >= -1) & (samples[:, 0] <= 1))
        assert all((samples[:, 1] >= 0) & (samples[:, 1] <= 2))

    def test_sample_batch(self, sampler, params, caplog):
        with caplog.at_level(logging.DEBUG, logger="uncharted.samplers.random"):
            samples = sampler.sample_batch(params, 100)
        assert samples.shape == (100, 2)
        assert all((samples[:, 0] >= -1) & (samples[:, 0] <= 1))
        assert all((samples[:, 1] >= 0) & (samples[:, 1] <= 2))
