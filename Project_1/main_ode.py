# main script for the ODE (coupled oscillator) part
# runs all four experiments and saves the figures for the report

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

from src.ode_integrators import integrate
from src.coupled_oscillator import rhs, exact_solution, energy, omega_plus, omega_minus


# make sure the figures folder exists
os.makedirs("figures")


# first experiment: compare my Euler, my RK4, scipy and the exact solution
# I start with only mass 1 displaced, so both normal modes get excited
# and I can see how each method tracks the motion over 30 time units.
print("experiment 1: compare methods")
y0 = np.array([1.0, 0.0, 0.0, 0.0])
t_end = 30.0
h = 0.05

ts, ys_euler = integrate(rhs, 0.0, y0, t_end, h, method="euler")
ts, ys_rk4 = integrate(rhs, 0.0, y0, t_end, h, method="rk4")

# scipy as a high-accuracy reference (basically "truth" at these tolerances)
t_fine = np.linspace(0.0, t_end, 2000)
sol = solve_ivp(rhs, (0.0, t_end), y0, t_eval=t_fine,
                method="DOP853", rtol=1e-10, atol=1e-12)
ys_scipy = sol.y.T

# analytic solution on the same fine grid
y_exact = exact_solution(t_fine, y0)

# plot x1(t) only (x2 looks similar)
plt.plot(t_fine, y_exact[:, 0], "k-", label="exact")
plt.plot(t_fine, ys_scipy[:, 0], "g--", label="scipy DOP853")
plt.plot(ts, ys_rk4[:, 0], "b.", label="RK4 mine")
plt.plot(ts, ys_euler[:, 0], "r.", label="Euler mine")
plt.xlabel("time")
plt.ylabel("x1(t)")
plt.title("Coupled oscillator solutions")
plt.legend()
plt.savefig("figures/ode_solutions.png")
plt.close()

# second experiment: energy conservation (physical test 1 from my plan)
# There is no friction, so total energy should stay constant.
# Any drift in E(t) is coming from the numerical method, not physics.
# For an oscillator, Euler is known to be unstable -> energy grows.
# RK4 is much better but also not exactly energy-conserving.
print("experiment 2: energy conservation")

ts, ys_euler = integrate(rhs, 0.0, y0, t_end, h, method="euler")
ts, ys_rk4 = integrate(rhs, 0.0, y0, t_end, h, method="rk4")

E0 = energy(y0)
E_euler = energy(ys_euler)
E_rk4 = energy(ys_rk4)

# top plot: linear scale, shows Euler blowing up
plt.subplot(2, 1, 1)
plt.plot(ts, E_euler / E0, "r-", label="Euler")
plt.plot(ts, E_rk4 / E0, "b-", label="RK4")
plt.axhline(1.0, color="k", linestyle=":")
plt.ylabel("E(t) / E(0)")
plt.legend()

# bottom plot: log scale, shows tiny RK4 drift I couldn't see above
plt.subplot(2, 1, 2)
plt.plot(ts, np.abs(E_rk4 - E0) / E0, "b-", label="RK4")
plt.yscale("log")
plt.ylabel("|E(t) - E(0)| / E(0)")
plt.xlabel("time")
plt.legend()

plt.tight_layout()
plt.savefig("figures/ode_energy.png")
plt.close()


# third experiment: beating pattern (physical test 2 from my plan)
# When I displace only one mass, both normal modes get equal amplitude.
# Their sum is a fast oscillation at the average frequency
# modulated by a slow envelope at the difference frequency (omega_- - omega_+)/2.
# So I should see x1(t) hugging that slow envelope.
print("experiment 3: beating")

y0 = np.array([1.0, 0.0, 0.0, 0.0])
t_end = 60.0
h = 0.05

ts, ys = integrate(rhs, 0.0, y0, t_end, h, method="rk4")
y_exact = exact_solution(ts, y0)

# slow envelope frequency from the identity
# cos(a) + cos(b) = 2 * cos((b-a)/2) * cos((b+a)/2)
omega_beat = 0.5 * (omega_minus - omega_plus)
envelope = np.cos(omega_beat * ts)

plt.plot(ts, ys[:, 0], "b-", label="x1 RK4")
plt.plot(ts, y_exact[:, 0], "k--", label="x1 exact")
plt.plot(ts, envelope, "r:", label="beat envelope")
plt.plot(ts, -envelope, "r:")
plt.xlabel("time")
plt.ylabel("x1(t)")
plt.title("Beating from single-mass IC")
plt.legend()
plt.savefig("figures/ode_beating.png")
plt.close()


# fourth experiment: convergence study
# Global error at t_end should scale like h^p with p = order of the method.
# For Euler p = 1 and for RK4 p = 4.
# I use short t_end = 5 here because Euler is unstable for oscillators.
# For long t_end the amplitude drift dominates and spoils the slope,
# I want to see the pure truncation-error scaling.
print("experiment 4: convergence")

y0 = np.array([1.0, 0.0, 0.0, 0.0])
t_end = 5.0
ns = np.array([50, 100, 200, 400, 800, 1600, 3200, 6400, 12800, 25600])
hs = t_end / ns

y_true = exact_solution(np.array([t_end]), y0)[0]

err_e = []
err_r = []
for h in hs:
    ts, y_e = integrate(rhs, 0.0, y0, t_end, h, method="euler")
    ts, y_r = integrate(rhs, 0.0, y0, t_end, h, method="rk4")
    err_e.append(np.linalg.norm(y_e[-1] - y_true, np.inf))
    err_r.append(np.linalg.norm(y_r[-1] - y_true, np.inf))
err_e = np.array(err_e)
err_r = np.array(err_r)

# reference slope lines to compare against
mid = len(hs) // 2
ref_e = err_e[mid] * (hs / hs[mid])       # slope 1
ref_r = err_r[mid] * (hs / hs[mid]) ** 4  # slope 4

plt.loglog(hs, err_e, "ro-", label="Euler")
plt.loglog(hs, err_r, "bs-", label="RK4")
plt.loglog(hs, ref_e, "r:", label="slope 1")
plt.loglog(hs, ref_r, "b:", label="slope 4")
plt.xlabel("step size h")
plt.ylabel("|error at t_end|")
plt.title("ODE convergence")
plt.legend()
plt.savefig("figures/ode_convergence.png")
plt.close()

# check the slopes are close to 1 and 4
# skip the coarsest 2 Euler points (still slightly unstable there)
# and skip the finest RK4 points (hit floating-point precision)
slope_e = np.polyfit(np.log(hs[2:]), np.log(err_e[2:]), 1)[0]
mask = err_r > 1e-12
slope_r = np.polyfit(np.log(hs[mask]), np.log(err_r[mask]), 1)[0]
print("Euler slope =", slope_e)
print("RK4 slope   =", slope_r)


# fifth experiment: local (one step) error scaling
# The convergence test above measures GLOBAL error at the end of the run.
# But the assignment also asks me to check the LOCAL (one step) error.
# From Section 4 of the report, theory says:
# Euler local error goes like h^2
# RK4 local error goes like h^5
# I check this by taking ONE step of each method from t=0 with different h
# and comparing to the exact solution at that same h.
print("experiment 5: local one step error")

from src.ode_integrators import euler_step, rk4_step

y0 = np.array([1.0, 0.0, 0.0, 0.0])
hs_local = np.array([0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625, 0.0078125])

err_e_local = []
err_r_local = []
for h in hs_local:
    y_e = euler_step(rhs, 0.0, y0, h)   # one step of Euler
    y_r = rk4_step(rhs, 0.0, y0, h)     # one step of RK4
    y_true = exact_solution(np.array([h]), y0)[0]
    err_e_local.append(np.linalg.norm(y_e - y_true, np.inf))
    err_r_local.append(np.linalg.norm(y_r - y_true, np.inf))

err_e_local = np.array(err_e_local)
err_r_local = np.array(err_r_local)

# reference lines with slopes 2 and 5
ref_e_local = err_e_local[0] * (hs_local / hs_local[0]) ** 2
ref_r_local = err_r_local[0] * (hs_local / hs_local[0]) ** 5

plt.loglog(hs_local, err_e_local, "ro-", label="Euler")
plt.loglog(hs_local, err_r_local, "bs-", label="RK4")
plt.loglog(hs_local, ref_e_local, "r:", label="slope 2")
plt.loglog(hs_local, ref_r_local, "b:", label="slope 5")
plt.xlabel("step size h")
plt.ylabel("|error after 1 step|")
plt.title("ODE local (one step) error")
plt.legend()
plt.savefig("figures/ode_local_error.png")
plt.close()

# check the slopes are close to 2 and 5
slope_e_local = np.polyfit(np.log(hs_local), np.log(err_e_local), 1)[0]
mask = err_r_local > 1e-14
slope_r_local = np.polyfit(np.log(hs_local[mask]), np.log(err_r_local[mask]), 1)[0]
print("Euler local slope =", slope_e_local)
print("RK4 local slope   =", slope_r_local)


print("done (I wanna make sure)")