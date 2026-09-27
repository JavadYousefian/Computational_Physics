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





def experiment_energy():
    # physical test 1: energy conservation
    # Euler grows a lot, RK4 stays almost flat
    y0 = np.array([1.0, 0.0, 0.0, 0.0])
    t_end = 30.0
    h = 0.05

    ts, ys_euler = integrate(rhs, 0.0, y0, t_end, h, method="euler")
    ts, ys_rk4 = integrate(rhs, 0.0, y0, t_end, h, method="rk4")

    E0 = energy(y0)
    E_euler = energy(ys_euler)
    E_rk4 = energy(ys_rk4)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.5, 5.5), sharex=True)

    ax1.plot(ts, E_euler / E0, "r-", label=f"Euler (h={h})")
    ax1.plot(ts, E_rk4 / E0, "b-", label=f"RK4 (h={h})")
    ax1.axhline(1.0, color="k", linestyle=":")
    ax1.set_ylabel("E(t) / E(0)")
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    ax2.plot(ts, np.abs(E_rk4 - E0) / E0, "b-", label=f"RK4 (h={h})")
    ax2.set_yscale("log")
    ax2.set_ylabel("|E(t) - E(0)| / E(0)")
    ax2.set_xlabel("time")
    ax2.grid(True, which="both", alpha=0.3)
    ax2.legend()

    fig.suptitle("Energy conservation")
    fig.tight_layout()

    path = os.path.join(fig_dir, "ode_energy.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"saved {path}")

def experiment_beating():
    # physical test 2: single mass IC excites both modes -> beating pattern
    # slow envelope frequency = (omega_minus - omega_plus) / 2
    from src.coupled_oscillator import omega_plus, omega_minus

    y0 = np.array([1.0, 0.0, 0.0, 0.0])
    t_end = 60.0
    h = 0.05

    ts, ys = integrate(rhs, 0.0, y0, t_end, h, method="rk4")
    y_exact = exact_solution(ts, y0)

    omega_beat = 0.5 * (omega_minus - omega_plus)
    envelope = np.cos(omega_beat * ts)

    fig, ax = plt.subplots(figsize=(8.0, 4.0))
    ax.plot(ts, ys[:, 0], "b-", label="x1 (RK4)", linewidth=0.9)
    ax.plot(ts, y_exact[:, 0], "k--", label="x1 (exact)", linewidth=0.7)
    ax.plot(ts, envelope, "r:", label="beat envelope")
    ax.plot(ts, -envelope, "r:")
    ax.set_xlabel("time")
    ax.set_ylabel("x1(t)")
    ax.set_title("Beating from single-mass initial condition")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()

    path = os.path.join(fig_dir, "ode_beating.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"saved {path}")




def experiment_convergence():
    # convergence study
    # expect Euler slope 1, RK4 slope 4
    # use short t_end = 5 so Euler amplitude drift doesn't spoil the slope
    y0 = np.array([1.0, 0.0, 0.0, 0.0])
    t_end = 5.0
    ns = np.array([50, 100, 200, 400, 800, 1600, 3200, 6400, 12800, 25600])
    hs = t_end / ns

    y_true = exact_solution(np.array([t_end]), y0)[0]

    err_e = np.empty_like(hs)
    err_r = np.empty_like(hs)
    for i, h in enumerate(hs):
        _, y_e = integrate(rhs, 0.0, y0, t_end, h, method="euler")
        _, y_r = integrate(rhs, 0.0, y0, t_end, h, method="rk4")
        err_e[i] = np.linalg.norm(y_e[-1] - y_true, np.inf)
        err_r[i] = np.linalg.norm(y_r[-1] - y_true, np.inf)

    mid = len(hs) // 2
    ref_e = err_e[mid] * (hs / hs[mid]) ** 1
    ref_r = err_r[mid] * (hs / hs[mid]) ** 4

    fig, ax = plt.subplots(figsize=(7.0, 5.0))
    ax.loglog(hs, err_e, "ro-", label="Euler")
    ax.loglog(hs, err_r, "bs-", label="RK4")
    ax.set_xlabel("step size h")
    ax.set_ylabel("|error at t_end|")
    ax.set_title(f"ODE convergence (t_end = {t_end})")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()

    path = os.path.join(fig_dir, "ode_convergence.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"saved {path}")

    # print slopes
    slope_e = np.polyfit(np.log(hs[2:]), np.log(err_e[2:]), 1)[0]
    mask = err_r > 1e-12
    slope_r = np.polyfit(np.log(hs[mask]), np.log(err_r[mask]), 1)[0]
    print(f"  Euler slope = {slope_e:.3f}")
    print(f"  RK4 slope   = {slope_r:.3f}")



experiment_solutions()
experiment_energy()
experiment_beating()
experiment_convergence()