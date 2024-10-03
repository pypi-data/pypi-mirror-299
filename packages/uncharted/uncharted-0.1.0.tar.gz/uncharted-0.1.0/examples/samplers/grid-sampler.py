"""Example of using the GridSampler to explore a function with two parameters."""

import numpy as np
import matplotlib.pyplot as plt
import uncharted
from uncharted.criteria import MaxSamples
from uncharted.samplers.grid import GridSampler


def f(x: np.ndarray) -> np.float64:
    return np.linalg.norm(x, axis=-1)


params = [uncharted.Parameter(-1, 1, step=0.2), uncharted.Parameter(-2, 2, step=0.2)]
explorer = uncharted.Explorer(params, GridSampler(shuffle=True), criteria=[MaxSamples(100)])
results = explorer.explore(f, 10)

plt.subplot(aspect="equal")
plt.scatter(results.x[:, 0], results.x[:, 1], c=results.y)
plt.show()
