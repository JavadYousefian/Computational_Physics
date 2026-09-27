# check the two physical behaviors from my plan:
# 1) short time  T << tau  ->  x(T) ~ v0*T   (like free motion)
# 2) long time   T -> inf  ->  x(T) -> v0*tau  (finite stopping distance)

import numpy as np
import matplotlib.pyplot as plt
from src.quad_integrators import simpson
from src.drag_stopping import velocity, exact_distance, v0, tau


# range of T values
Ts = np.linspace(0.01, 20 * tau, 100)

# numerical (Simpson) and exact
numeric = np.array([simpson(velocity, 0.0, T, 64) for T in Ts])
exact = np.array([exact_distance(T) for T in Ts])

plt.plot(Ts / tau, exact, "k-", label="exact")
plt.plot(Ts / tau, numeric, "b.", label="Simpson")
plt.axhline(v0 * tau, color="r", linestyle=":", label=f"v0*tau = {v0*tau}")
plt.plot(Ts / tau, v0 * Ts, "g--", label="v0*T (no drag)")
plt.xlabel("T / tau")
plt.ylabel("x(T)")
plt.title("Stopping distance vs T")
plt.legend()
plt.ylim(0, 1.3 * v0 * tau)
plt.show()