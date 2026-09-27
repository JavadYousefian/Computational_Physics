# main script for the ODE (coupled oscillator) part
# produces all figures needed for the report

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

from src.ode_integrators import integrate
from src.coupled_oscillator import rhs, exact_solution, energy


# where figures are saved
fig_dir = os.path.join("report", "figures")
os.makedirs(fig_dir, exist_ok=True)



def experiment_solutions():
    # compare my Euler, my RK4, scipy, and exact solution
    y0 = np.array([1.0, 0.0, 0.0, 0.0])
    t_end = 30.0
    h = 0.05

    ts, ys_euler = integrate(rhs, 0.0, y0, t_end, h, method="euler")
    ts, ys_rk4 = integrate(rhs, 0.0, y0, t_end, h, method="rk4")

    # scipy reference at fine grid
    t_fine = np.linspace(0.0, t_end, 2000)
    sol = solve_ivp(rhs, (0.0, t_end), y0, t_eval=t_fine,
                    method="DOP853", rtol=1e-10, atol=1e-12)
    ys_scipy = sol.y.T
    y_exact = exact_solution(t_fine, y0)

    fig, axes = plt.subplots(2, 1, figsize=(7.5, 5.5), sharex=True)
    for i, label in enumerate(("x1(t)", "x2(t)")):
        ax = axes[i]
        ax.plot(t_fine, y_exact[:, i], "k-", label="exact", linewidth=1.2)
        ax.plot(t_fine, ys_scipy[:, i], "0.55", linestyle="--",
                label="scipy DOP853")
        ax.plot(ts, ys_rk4[:, i], "b.", markersize=2.5, label=f"RK4 (h={h})")
        ax.plot(ts, ys_euler[:, i], "r.", markersize=2.5, label=f"Euler (h={h})")
        ax.set_ylabel(label)
        ax.grid(True, alpha=0.3)
    axes[0].legend(loc="upper right", ncol=2, fontsize=8)
    axes[1].set_xlabel("time")
    fig.suptitle("Coupled oscillator: comparison of methods")
    fig.tight_layout()

    path = os.path.join(fig_dir, "ode_solutions.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"saved {path}")



experiment_solutions()