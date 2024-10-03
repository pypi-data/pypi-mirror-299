"""Classes for specifying parameters and spaces to explore."""

from collections.abc import Sequence
from dataclasses import dataclass
from functools import cached_property
from itertools import product

import numpy as np
from loguru import logger


@dataclass
class Parameter:
    """Dataclass for specifying parameters to explore."""

    min_value: float
    max_value: float
    nominal: float | None = None
    step: float | None = None
    name: str | None = None
    # TODO: consider how to handle logarithmic parameters

    def __post_init__(self):
        """Fully initialize the parameter."""
        if self.nominal is None:
            self.nominal = (self.min_value + self.max_value) / 2
            logger.debug(f"Setting nominal value to {self.nominal}")

    def get_array(self):
        """Get an array of values for this parameter."""
        return np.arange(self.min_value, self.max_value + self.step / 2, self.step)


@dataclass(frozen=True)
class ParameterSpace:
    """Dataclass for a parameter space to explore."""

    parameters: Sequence[Parameter]

    def __len__(self) -> int:
        """Return the number of parameters in the parameter space."""
        return len(self.parameters)

    def __iter__(self):
        """Iterate over the parameter space."""
        return iter(self.parameters)

    @cached_property
    def limits(self) -> tuple[tuple, tuple]:
        """Get the min and max values for each parameter."""
        return tuple(zip(*((p.min_value, p.max_value) for p in self.parameters)))

    @cached_property
    def corners(self) -> tuple[tuple, tuple]:
        """Get the corner values of the parameter space."""
        return list(product(*((p.min_value, p.max_value) for p in self.parameters)))

    def get_arrays(self):
        """Get an array of values for each parameter."""
        return tuple(d.get_array() for d in self.parameters)
