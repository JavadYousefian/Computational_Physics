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

experiment_solutions()