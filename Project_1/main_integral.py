# main script for the integral (drag stopping distance) part
# runs the three experiments and saves the figures for the report

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import trapezoid as scipy_trap
from scipy.integrate import simpson as scipy_simp

from src.quad_integrators import riemann, trapezoid, simpson
from src.drag_stopping import velocity, exact_distance, v0, tau


# make sure the figures folder exists
os.makedirs("report/figures", exist_ok=True)


# first experiment: compare all three rules to the exact answer at fixed n
# The integral I want is x(T) = integral from 0 to T of v0*exp(-t/tau) dt.
# Analytic answer: x(T) = v0*tau*(1 - exp(-T/tau)).
# So I know the exact value and can measure the error of each rule.
print("experiment 1: fixed n")
T = 3.0
n = 32
exact = exact_distance(T)

r = riemann(velocity, 0.0, T, n)
t = trapezoid(velocity, 0.0, T, n)
s = simpson(velocity, 0.0, T, n)

# scipy versions on the same grid (should match mine exactly)
xs = np.linspace(0.0, T, n + 1)
ys = velocity(xs)
t_scipy = scipy_trap(ys, xs)
s_scipy = scipy_simp(ys, x=xs)

print("exact =", exact)
print("Riemann mine   =", r, "  error =", r - exact)
print("Trapezoid mine =", t, "  error =", t - exact)
print("Trapezoid scipy=", t_scipy, "  error =", t_scipy - exact)
print("Simpson mine   =", s, "  error =", s - exact)
print("Simpson scipy  =", s_scipy, "  error =", s_scipy - exact)

# plot the integrand v(t) with the grid points on top
t_plot = np.linspace(0.0, T, 200)
plt.plot(t_plot, velocity(t_plot), "k-", label="v(t)")
plt.plot(xs, velocity(xs), "ro", label="grid points")
plt.xlabel("time")
plt.ylabel("velocity")
plt.title("Stopping distance integrand")
plt.legend()
plt.savefig("report/figures/integral_solutions.png")
plt.close()


# second experiment: convergence study
# Each rule has an expected global error scaling like h^p:
#   Riemann (left):   p = 1
#   Trapezoid:        p = 2
#   Simpson:          p = 4
# So on a log-log plot of |error| vs step size h, I should see straight
# lines with slopes 1, 2, 4.
print("experiment 2: convergence")
T = 3.0
exact = exact_distance(T)

ns = np.array([4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048])
hs = T / ns

err_r = []
err_t = []
err_s = []
err_t_scipy = []
err_s_scipy = []

for n in ns:
    err_r.append(abs(riemann(velocity, 0.0, T, n) - exact))
    err_t.append(abs(trapezoid(velocity, 0.0, T, n) - exact))
    err_s.append(abs(simpson(velocity, 0.0, T, n) - exact))
    xs = np.linspace(0.0, T, n + 1)
    ys = velocity(xs)
    err_t_scipy.append(abs(scipy_trap(ys, xs) - exact))
    err_s_scipy.append(abs(scipy_simp(ys, x=xs) - exact))

err_r = np.array(err_r)
err_t = np.array(err_t)
err_s = np.array(err_s)
err_t_scipy = np.array(err_t_scipy)
err_s_scipy = np.array(err_s_scipy)

# reference slope lines
ref_r = err_r[0] * (hs / hs[0])
ref_t = err_t[0] * (hs / hs[0]) ** 2
ref_s = err_s[0] * (hs / hs[0]) ** 4

plt.loglog(hs, err_r, "ro-", label="Riemann mine")
plt.loglog(hs, err_t, "bs-", label="Trapezoid mine")
plt.loglog(hs, err_s, "g^-", label="Simpson mine")
plt.loglog(hs, err_t_scipy, "bx", label="Trapezoid scipy")
plt.loglog(hs, err_s_scipy, "g+", label="Simpson scipy")
plt.loglog(hs, ref_r, "r:", label="slope 1")
plt.loglog(hs, ref_t, "b:", label="slope 2")
plt.loglog(hs, ref_s, "g:", label="slope 4")
plt.xlabel("step size h")
plt.ylabel("|error|")
plt.title("Quadrature convergence")
plt.legend()
plt.savefig("report/figures/integral_convergence.png")
plt.close()

# fit slopes to check they match 1, 2, 4
slope_r = np.polyfit(np.log(hs), np.log(err_r), 1)[0]
slope_t = np.polyfit(np.log(hs), np.log(err_t), 1)[0]
# for Simpson skip the smallest h where error hits machine precision
mask = err_s > 1e-13
slope_s = np.polyfit(np.log(hs[mask]), np.log(err_s[mask]), 1)[0]
print("Riemann slope   =", slope_r)
print("Trapezoid slope =", slope_t)
print("Simpson slope   =", slope_s)


# third experiment: physical limits from my plan
# Short time (T << tau): the object hasn't slowed much yet, so
#   x(T) ~ v0*T   (like free motion with no drag)
# Long time (T -> infinity): the object never fully stops but the total
# distance is finite. From the exact formula:
#   x_infinity = v0*tau
# So the numerical curve should approach v0*tau as T grows.
print("experiment 3: physical limits")

Ts = np.linspace(0.01, 20.0 * tau, 40)

# for each T, run Simpson with enough sub-intervals (must be even)
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

# left plot: full curve with both asymptotes overlaid
plt.subplot(1, 2, 1)
plt.plot(Ts / tau, exact, "k-", label="exact")
plt.plot(Ts / tau, numeric, "bo", label="Simpson")
plt.axhline(v0 * tau, color="r", linestyle=":", label="v0*tau")
plt.plot(Ts / tau, v0 * Ts, "g--", label="v0*T (no drag)")
plt.xlabel("T / tau")
plt.ylabel("x(T)")
plt.ylim(0.0, 1.3 * v0 * tau)
plt.title("Approach to asymptote")
plt.legend()

# right plot: how much x(T) deviates from v0*T at short times
small_Ts = np.linspace(0.001, 0.5, 30) * tau
small_num = np.array([simpson(velocity, 0.0, T, 32) for T in small_Ts])
deviation = (small_num - v0 * small_Ts) / (v0 * small_Ts)

plt.subplot(1, 2, 2)
plt.plot(small_Ts / tau, deviation, "bo-")
plt.xlabel("T / tau")
plt.ylabel("(x_num - v0*T) / (v0*T)")
plt.title("Short-time deviation")

plt.tight_layout()
plt.savefig("report/figures/integral_limits.png")
plt.close()


# fourth experiment: local (one step) error scaling
# The convergence test above measures GLOBAL error over the whole interval.
# But the assignment also asks me to check the LOCAL error (error on one
# sub-interval, before adding up all the sub-intervals).
# From Section 4 of the report, theory says:
#   Riemann local error goes like h^2
#   Trapezoid local error goes like h^3
#   Simpson local error goes like h^5
# I check this by applying each rule to just ONE sub-interval of width h
# (or a pair 2h for Simpson because it needs even n) and comparing to the
# exact integral over that same small interval.
print("experiment 4: local error")

hs_local = np.array([0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625, 0.0078125])

err_ri_local = []
err_tr_local = []
err_si_local = []
for h in hs_local:
    # Riemann and trapezoid: apply on [0, h] with 1 sub-interval
    exact_h = exact_distance(h)
    err_ri_local.append(abs(riemann(velocity, 0.0, h, 1) - exact_h))
    err_tr_local.append(abs(trapezoid(velocity, 0.0, h, 1) - exact_h))
    # Simpson needs even n, so apply on [0, 2h] with n=2 (one pair of intervals)
    exact_2h = exact_distance(2 * h)
    err_si_local.append(abs(simpson(velocity, 0.0, 2 * h, 2) - exact_2h))

err_ri_local = np.array(err_ri_local)
err_tr_local = np.array(err_tr_local)
err_si_local = np.array(err_si_local)

# reference lines with slopes 2, 3, 5
ref_ri_local = err_ri_local[0] * (hs_local / hs_local[0]) ** 2
ref_tr_local = err_tr_local[0] * (hs_local / hs_local[0]) ** 3
ref_si_local = err_si_local[0] * (hs_local / hs_local[0]) ** 5

plt.loglog(hs_local, err_ri_local, "ro-", label="Riemann")
plt.loglog(hs_local, err_tr_local, "bs-", label="Trapezoid")
plt.loglog(hs_local, err_si_local, "g^-", label="Simpson")
plt.loglog(hs_local, ref_ri_local, "r:", label="slope 2")
plt.loglog(hs_local, ref_tr_local, "b:", label="slope 3")
plt.loglog(hs_local, ref_si_local, "g:", label="slope 5")
plt.xlabel("step size h")
plt.ylabel("|error on 1 sub-interval|")
plt.title("Quadrature local error")
plt.legend()
plt.savefig("report/figures/integral_local_error.png")
plt.close()

# check the slopes are close to 2, 3, 5
slope_ri_local = np.polyfit(np.log(hs_local), np.log(err_ri_local), 1)[0]
slope_tr_local = np.polyfit(np.log(hs_local), np.log(err_tr_local), 1)[0]
mask = err_si_local > 1e-14
slope_si_local = np.polyfit(np.log(hs_local[mask]), np.log(err_si_local[mask]), 1)[0]
print("Riemann local slope   =", slope_ri_local)
print("Trapezoid local slope =", slope_tr_local)
print("Simpson local slope   =", slope_si_local)


print("done")