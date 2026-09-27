# check if energy is conserved
# for RK4 should be almost flat
# for Euler should grow (unstable on oscillator)

import numpy as np
import matplotlib.pyplot as plt
from src.ode_integrators import integrate
from src.coupled_oscillator import rhs, energy


y0 = np.array([1.0, 0.0, 0.0, 0.0])
t_end = 30.0
h = 0.05

ts, ys_euler = integrate(rhs, 0.0, y0, t_end, h, method="euler")
ts, ys_rk4 = integrate(rhs, 0.0, y0, t_end, h, method="rk4")

E0 = energy(y0)
E_euler = energy(ys_euler)
E_rk4 = energy(ys_rk4)

plt.plot(ts, E_euler / E0, "r-", label="Euler")
plt.plot(ts, E_rk4 / E0, "b-", label="RK4")
plt.axhline(1.0, color="k", linestyle=":", label="exact (=1)")
plt.xlabel("time")
plt.ylabel("E(t) / E(0)")
plt.title("Energy conservation check")
plt.legend()
plt.show()