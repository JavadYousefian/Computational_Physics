# convergence study for the three quadrature rules

import numpy as np
import matplotlib.pyplot as plt
from src.quad_integrators import riemann, trapezoid, simpson
from src.drag_stopping import velocity, exact_distance


T = 3.0
exact = exact_distance(T)

# try many n values (all even for Simpson)
ns = np.array([4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048])
hs = T / ns

err_r = np.array([abs(riemann(velocity, 0.0, T, n) - exact) for n in ns])
err_t = np.array([abs(trapezoid(velocity, 0.0, T, n) - exact) for n in ns])
err_s = np.array([abs(simpson(velocity, 0.0, T, n) - exact) for n in ns])

# reference lines
ref_r = err_r[0] * (hs / hs[0]) ** 1
ref_t = err_t[0] * (hs / hs[0]) ** 2
ref_s = err_s[0] * (hs / hs[0]) ** 4

plt.loglog(hs, err_r, "ro-", label="Riemann")
plt.loglog(hs, err_t, "bs-", label="Trapezoid")
plt.loglog(hs, err_s, "g^-", label="Simpson")
plt.xlabel("step size h")
plt.ylabel("|error|")
plt.title("Quadrature convergence")
plt.legend()
plt.grid(True, which="both", alpha=0.3)
plt.show()

# also fit slopes to check numbers
slope_r = np.polyfit(np.log(hs), np.log(err_r), 1)[0]
slope_t = np.polyfit(np.log(hs), np.log(err_t), 1)[0]
# exclude tiny Simpson errors (they hit machine precision)
mask = err_s > 1e-13
slope_s = np.polyfit(np.log(hs[mask]), np.log(err_s[mask]), 1)[0]
print(f"Riemann slope   = {slope_r:.3f}")
print(f"Trapezoid slope = {slope_t:.3f}")
print(f"Simpson slope   = {slope_s:.3f}")