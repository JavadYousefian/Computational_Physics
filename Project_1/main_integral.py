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
    plt.xlabel("step size h")
    plt.ylabel("|error|")
    plt.title("Quadrature convergence")
    plt.legend(fontsize=7)

    path = os.path.join(fig_dir, "integral_convergence.png")
    plt.savefig(path)
    plt.close()
    print("saved", path)

    # print slopes
    slope_r = np.polyfit(np.log(hs), np.log(err_r), 1)[0]
    slope_t = np.polyfit(np.log(hs), np.log(err_t), 1)[0]
    mask = err_s > 1e-13
    slope_s = np.polyfit(np.log(hs[mask]), np.log(err_s[mask]), 1)[0]
    print("  Riemann slope   =", slope_r)
    print("  Trapezoid slope =", slope_t)
    print("  Simpson slope   =", slope_s)





def experiment_limits():
    # check the two physical limits from my plan:
    # short time  T << tau  ->  x(T) ~ v0*T
    # long time   T -> inf  ->  x(T) -> v0*tau

    # range of T
    Ts = np.linspace(0.01, 20.0 * tau, 40)

    # use Simpson with even n (careful, n must be even)
    numeric = []
    for T in Ts:
        n = int(20 * T / tau)
        if n < 4:
            n = 4
        if n % 2 != 0:
            n = n + 1
        numeric.append(simpson(velocity, 0.0, T, n))
    numeric = np.array(numeric)

    exact = np.array([exact_distance(T) for T in Ts])

    # two side-by-side plots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))

    # left: full curve with both asymptotes
    ax1.plot(Ts / tau, exact, "k-", label="exact")
    ax1.plot(Ts / tau, numeric, "bo", markersize=3, label="Simpson")
    ax1.axhline(v0 * tau, color="r", linestyle=":", label="v0*tau")
    ax1.plot(Ts / tau, v0 * Ts, "g--", label="v0*T (no drag)")
    ax1.set_xlabel("T / tau")
    ax1.set_ylabel("x(T)")
    ax1.set_ylim(0.0, 1.3 * v0 * tau)
    ax1.set_title("Approach to asymptote")
    ax1.legend(fontsize=8)

    # right: short time deviation from v0*T
    small_Ts = np.linspace(0.001, 0.5, 30) * tau
    small_num = np.array([simpson(velocity, 0.0, T, 32) for T in small_Ts])
    deviation = (small_num - v0 * small_Ts) / (v0 * small_Ts)
    ax2.plot(small_Ts / tau, deviation, "bo-", markersize=3)
    ax2.set_xlabel("T / tau")
    ax2.set_ylabel("(x_num - v0*T) / (v0*T)")
    ax2.set_title("Short-time deviation")

    plt.tight_layout()
    path = os.path.join(fig_dir, "integral_limits.png")
    plt.savefig(path)
    plt.close()
    print("saved", path)


experiment_solutions()
experiment_convergence()
experiment_limits()