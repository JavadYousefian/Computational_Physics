# convergence study for Euler and RK4
# I use a shorter t_end (5) here so Euler amplitude drift is small enough to see the truncation error scaling clean.

import numpy as np
import matplotlib.pyplot as plt
from src.ode_integrators import integrate
from src.coupled_oscillator import rhs, exact_solution


y0 = np.array([1.0, 0.0, 0.0, 0.0])
t_end = 5.0

# use step sizes small enough for Euler to be stable
ns = np.array([50, 100, 200, 400, 800, 1600, 3200, 6400, 12800, 25600])
hs = t_end / ns

# exact solution at t_end
y_true = exact_solution(np.array([t_end]), y0)[0]

err_e = []
err_r = []
for h in hs:
    _, y_e = integrate(rhs, 0.0, y0, t_end, h, method="euler")
    _, y_r = integrate(rhs, 0.0, y0, t_end, h, method="rk4")
    err_e.append(np.linalg.norm(y_e[-1] - y_true, np.inf))
    err_r.append(np.linalg.norm(y_r[-1] - y_true, np.inf))

err_e = np.array(err_e)
err_r = np.array(err_r)

# reference lines
mid = len(hs) // 2
ref_e = err_e[mid] * (hs / hs[mid]) ** 1
ref_r = err_r[mid] * (hs / hs[mid]) ** 4

plt.loglog(hs, err_e, "ro-", label="Euler")
plt.loglog(hs, err_r, "bs-", label="RK4")
plt.xlabel("step size h")
plt.ylabel("|error at t_end|")
plt.title("ODE convergence (coupled oscillator)")
plt.legend()
plt.grid(True, which="both", alpha=0.3)
plt.show()

# fit slopes (skip the biggest h for Euler, skip machine-precision for RK4)
slope_e = np.polyfit(np.log(hs[2:]), np.log(err_e[2:]), 1)[0]
mask = err_r > 1e-12
slope_r = np.polyfit(np.log(hs[mask]), np.log(err_r[mask]), 1)[0]
print(f"Euler slope = {slope_e:.3f}")
print(f"RK4 slope   = {slope_r:.3f}")