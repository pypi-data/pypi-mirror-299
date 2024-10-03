"""Example of using the RandomSampler to explore a function with two parameters."""

import numpy as np
import uncharted
from uncharted.criteria import MaxSamples
from uncharted.samplers.random import RandomSampler, QMCSampler
import matplotlib.pyplot as plt


def f(x: np.ndarray) -> np.float64:
    return np.linalg.norm(x, axis=-1)


params = [uncharted.Parameter(-1, 1), uncharted.Parameter(-2, 2)]
explorer = uncharted.Explorer(params, QMCSampler(10, seed=0), criteria=[MaxSamples(100)])
results = explorer.explore(f, 10)

plt.subplot(aspect="equal")
plt.scatter(results.x[:, 0], results.x[:, 1], c=results.y)
plt.show()
