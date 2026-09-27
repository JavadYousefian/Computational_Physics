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



# normal-mode angular frequencies
omega_plus = np.sqrt(k / m)        # in-phase mode:  x1 = x2
omega_minus = np.sqrt(3 * k / m)   # out-of-phase mode:  x1 = -x2




def exact_solution(t, y0):

    t = np.asarray(t, dtype=float)
    x1_0, x2_0, v1_0, v2_0 = y0

    # project onto normal-mode coordinates
    q_plus_0 = (x1_0 + x2_0) / np.sqrt(2.0)
    q_minus_0 = (x1_0 - x2_0) / np.sqrt(2.0)
    p_plus_0 = (v1_0 + v2_0) / np.sqrt(2.0)
    p_minus_0 = (v1_0 - v2_0) / np.sqrt(2.0)

    # evolve each mode with cos and sin
    q_plus = q_plus_0 * np.cos(omega_plus * t) + (p_plus_0 / omega_plus) * np.sin(omega_plus * t)
    q_minus = q_minus_0 * np.cos(omega_minus * t) + (p_minus_0 / omega_minus) * np.sin(omega_minus * t)
    p_plus = -q_plus_0 * omega_plus * np.sin(omega_plus * t) + p_plus_0 * np.cos(omega_plus * t)
    p_minus = -q_minus_0 * omega_minus * np.sin(omega_minus * t) + p_minus_0 * np.cos(omega_minus * t)

    # rotate back to physical (x1, x2, v1, v2) basis
    x1 = (q_plus + q_minus) / np.sqrt(2.0)
    x2 = (q_plus - q_minus) / np.sqrt(2.0)
    v1 = (p_plus + p_minus) / np.sqrt(2.0)
    v2 = (p_plus - p_minus) / np.sqrt(2.0)

    return np.stack([x1, x2, v1, v2], axis=-1)