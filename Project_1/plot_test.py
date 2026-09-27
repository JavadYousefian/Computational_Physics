# quick plot to see if my methods match the exact solution

import numpy as np
import matplotlib.pyplot as plt
from src.ode_integrators import integrate
from src.coupled_oscillator import rhs, exact_solution


# IC: only mass 1 displaced
y0 = np.array([1.0, 0.0, 0.0, 0.0])
t_end = 20.0
h = 0.1

# my methods
ts, ys_euler = integrate(rhs, 0.0, y0, t_end, h, method="euler")
ts, ys_rk4 = integrate(rhs, 0.0, y0, t_end, h, method="rk4")

# exact
y_exact = exact_solution(ts, y0)

# plot x1
plt.plot(ts, y_exact[:, 0], "k-", label="exact")
plt.plot(ts, ys_rk4[:, 0], "b.", label="RK4")
plt.plot(ts, ys_euler[:, 0], "r.", label="Euler")
plt.xlabel("time")
plt.ylabel("x1")
plt.legend()
plt.show()