# main script for the integral (drag stopping distance) part
# produces all figures needed for the report

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import trapezoid as scipy_trap
from scipy.integrate import simpson as scipy_simp

from src.quad_integrators import riemann, trapezoid, simpson
from src.drag_stopping import velocity, exact_distance, v0, tau


# where figures are saved
fig_dir = os.path.join("report", "figures")
os.makedirs(fig_dir, exist_ok=True)




def experiment_solutions():
    # compare all rules at fixed n and plot the integrand
    T = 3.0
    n = 32

    exact = exact_distance(T)

    r = riemann(velocity, 0.0, T, n)
    t = trapezoid(velocity, 0.0, T, n)
    s = simpson(velocity, 0.0, T, n)

    xs = np.linspace(0.0, T, n + 1)
    ys = velocity(xs)
    t_scipy = scipy_trap(ys, xs)
    s_scipy = scipy_simp(ys, x=xs)

    print("T =", T, "n =", n, "exact =", exact)
    print("Riemann (mine)   =", r, "  error =", r - exact)
    print("Trapezoid (mine) =", t, "  error =", t - exact)
    print("Trapezoid (scipy)=", t_scipy, "  error =", t_scipy - exact)
    print("Simpson (mine)   =", s, "  error =", s - exact)
    print("Simpson (scipy)  =", s_scipy, "  error =", s_scipy - exact)

    # plot v(t) and the grid points
    t_plot = np.linspace(0.0, T, 200)
    plt.plot(t_plot, velocity(t_plot), "k-", label="v(t)")
    plt.plot(xs, velocity(xs), "ro", label="grid points")
    plt.xlabel("time")
    plt.ylabel("velocity")
    plt.title("Stopping distance integrand")
    plt.legend()

    path = os.path.join(fig_dir, "integral_solutions.png")
    plt.savefig(path)
    plt.close()
    print("saved", path)



def experiment_convergence():
    # convergence study for the three rules
    # expect slopes: Riemann=1, Trapezoid=2, Simpson=4
    T = 3.0
    exact = exact_distance(T)

    ns = np.array([4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048])
    hs = T / ns

    err_r = np.array([abs(riemann(velocity, 0.0, T, n) - exact) for n in ns])
    err_t = np.array([abs(trapezoid(velocity, 0.0, T, n) - exact) for n in ns])
    err_s = np.array([abs(simpson(velocity, 0.0, T, n) - exact) for n in ns])

    # also compute scipy versions to check they match mine
    err_t_scipy = []
    err_s_scipy = []
    for n in ns:
        xs = np.linspace(0.0, T, n + 1)
        ys = velocity(xs)
        err_t_scipy.append(abs(scipy_trap(ys, xs) - exact))
        err_s_scipy.append(abs(scipy_simp(ys, x=xs) - exact))
    err_t_scipy = np.array(err_t_scipy)
    err_s_scipy = np.array(err_s_scipy)

    # reference lines
    ref_r = err_r[0] * (hs / hs[0]) ** 1
    ref_t = err_t[0] * (hs / hs[0]) ** 2
    ref_s = err_s[0] * (hs / hs[0]) ** 4

    plt.loglog(hs, err_r, "ro-", label="Riemann (mine)")
    plt.loglog(hs, err_t, "bs-", label="Trapezoid (mine)")
    plt.loglog(hs, err_s, "g^-", label="Simpson (mine)")
    plt.loglog(hs, err_t_scipy, "bx", label="Trapezoid (scipy)")
    plt.loglog(hs, err_s_scipy, "g+", label="Simpson (scipy)")
    plt.loglog(hs, ref_r, "r:", label="h^1")
    plt.loglog(hs, ref_t, "b:", label="h^2")
    plt.loglog(hs, ref_s, "g:", label="h^4")
    plt.xlabel("step size h")
    plt.ylabel("|error|")
    plt.title("Quadrature convergence")
    plt.legend(fontsize=7)

    path = os.path.join(FIG_DIR, "integral_convergence.png")
    plt.savefig(path)
    plt.close()
    print("saved", path)

    # print slopes
    slope_r = np.polyfit(np.log(hs), np.log(err_r), 1)[0]
    slope_t = np.polyfit(np.log(hs), np.log(err_t), 1)[0]
    mask = err_s > 1e-13
    slope_s = np.polyfit(np.log(hs[mask]), np.log(err_s[mask]), 1)[0]
    print("  Riemann slope   =", slope_r, "(expect 1)")
    print("  Trapezoid slope =", slope_t, "(expect 2)")
    print("  Simpson slope   =", slope_s, "(expect 4)")



experiment_solutions()
experiment_convergence()