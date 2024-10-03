"""Test the uncharted.explorer module."""

import pytest
import uncharted
import numpy as np
import uncharted.criteria
from loguru import logger

logger.enable("uncharted")


class TestResults:
    def test_init(self):
        results = uncharted.Results([0, 0], [1])
        assert results.x.shape == (1, 2)
        assert results.y.shape == (1,)

    def test_append(self):
        results = uncharted.Results([0, 0], [1])
        results.append([1, 1], 2)
        assert results.x.shape == (2, 2)
        assert results.y.shape == (2,)
        assert np.allclose(results.x, [[0, 0], [1, 1]])
        assert np.allclose(results.y, [1, 2])


@pytest.fixture
def params() -> list[uncharted.Parameter]:
    return [uncharted.Parameter(-1, 1), uncharted.Parameter(0, 2)]


class TestExplorer:
    @pytest.fixture
    def explorer(self, params) -> uncharted.Explorer:
        return uncharted.Explorer(params, sampler=uncharted.samplers.RandomSampler())

    def test_ask(self, explorer):
        assert explorer.ask().shape == (2,)

    def test_ask_n(self, explorer):
        assert explorer.ask(3).shape == (3, 2)

    def test_tell(self, explorer):
        explorer.tell([0, 0], 1)
        assert explorer.results.x.shape == (1, 2)
        assert explorer.results.y.shape == (1,)
        assert np.allclose(explorer.results.x, [(0, 0)])
        assert np.allclose(explorer.results.y, [1])

    def test_criteria(self, params, caplog):
        maxn = uncharted.criteria.MaxSamples(10)
        explorer = uncharted.Explorer(params, sampler=uncharted.samplers.RandomSampler(), criteria=[maxn])
        assert len(explorer.criteria) == 1

        with caplog.at_level("INFO"):
            results = explorer.explore(lambda x: x[0] + x[1], batch_size=1)
        assert len(results) == 10
        assert "Termination criterion met" in caplog.text
