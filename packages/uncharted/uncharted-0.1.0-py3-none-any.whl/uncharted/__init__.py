"""Uncharted: A package for exploring parameter spaces of unknown functions."""

from loguru import logger

from .explorer import Explorer, Results
from .parameters import Parameter
from .samplers import Sampler, StopExploration

__version__ = "0.1.0"
__all__ = ["Explorer", "Parameter", "Results", "Sampler", "StopExploration"]

logger.disable("uncharted")
