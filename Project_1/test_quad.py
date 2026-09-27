# test my three quadrature rules and compare to scipy where possible
# exact:  x(T) = v0 * tau * (1 - exp(-T/tau))

import numpy as np
from scipy.integrate import trapezoid as scipy_trap
from scipy.integrate import simpson as scipy_simp

from src.quad_integrators import riemann, trapezoid, simpson
from src.drag_stopping import velocity, exact_distance


T = 3.0
n = 32

exact = exact_distance(T)

# my rules
r = riemann(velocity, 0.0, T, n)
t = trapezoid(velocity, 0.0, T, n)
s = simpson(velocity, 0.0, T, n)

# scipy rules (need to give arrays of x and y values)
xs = np.linspace(0.0, T, n + 1)
ys = velocity(xs)
t_scipy = scipy_trap(ys, xs)
s_scipy = scipy_simp(ys, x=xs)

print(f"exact             = {exact:.10f}")
print(f"Riemann (mine)    = {r:.10f}   error = {r - exact:+.3e}")
print(f"Trapezoid (mine)  = {t:.10f}   error = {t - exact:+.3e}")
print(f"Trapezoid (scipy) = {t_scipy:.10f}   error = {t_scipy - exact:+.3e}")
print(f"Simpson (mine)    = {s:.10f}   error = {s - exact:+.3e}")
print(f"Simpson (scipy)   = {s_scipy:.10f}   error = {s_scipy - exact:+.3e}")