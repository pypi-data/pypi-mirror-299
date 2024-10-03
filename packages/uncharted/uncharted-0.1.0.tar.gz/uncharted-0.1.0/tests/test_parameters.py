"""Test the uncharted.parameters module."""

from uncharted.parameters import Parameter, ParameterSpace
import logging
import pytest

logger = logging.getLogger(__name__)

def test_parameter():
    p = Parameter(-1, 1)

class TestParameterSpace:
    @pytest.fixture
    def params(self):
        return ParameterSpace([Parameter(-1, 1), Parameter(0, 2)])

    def test_limits(self, params):
        minv, maxv = params.limits
        logger.info(f"{minv=}, {maxv=}")
        assert minv == (-1, 0)
        assert maxv == (1, 2)
