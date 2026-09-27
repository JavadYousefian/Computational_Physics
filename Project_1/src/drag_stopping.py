# Physics for the linear drag stopping distance problem.

# An object with initial speed v0 slows down under drag force F = -b*v.
# Solving Newton's second law gives  v(t) = v0 * exp(-t/tau)  where tau = m/b.

# Like before importing packages needed
import numpy as np

# physical parameters
v0 = 1.0    # initial speed
tau = 1.0   # time constant = m / b




def velocity(t):
    # v(t) = v0 * exp(-t/tau)
    # Based on my plan this is formula 4
    return v0 * np.exp(-np.asarray(t) / tau)


def exact_distance(T):
    # x(T) = integral from 0 to T of v(t) dt
    return v0 * tau * (1.0 - np.exp(-T / tau))