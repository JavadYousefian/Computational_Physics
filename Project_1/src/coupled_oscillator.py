# Physics for the two-mass, three-spring coupled oscillator.

import numpy as np


# physical parameters
m = 1.0   # mass
k = 1.0   # spring constant


def rhs(t, y):
    """Right-hand side for the coupled oscillator.
    State y = (x1, x2, v1, v2).
    Returns dy/dt.
    """
    x1, x2, v1, v2 = y
    a1 = (-2.0 * k * x1 + k * x2) / m
    a2 = (k * x1 - 2.0 * k * x2) / m
    return np.array([v1, v2, a1, a2])