# quick test: my three quadrature rules on the drag stopping distance
# exact answer known:  x(T) = v0 * tau * (1 - exp(-T/tau))

from src.quad_integrators import riemann, trapezoid, simpson
from src.drag_stopping import velocity, exact_distance


T = 3.0
n = 32

exact = exact_distance(T)
r = riemann(velocity, 0.0, T, n)
t = trapezoid(velocity, 0.0, T, n)
s = simpson(velocity, 0.0, T, n)

print(f"exact       = {exact:.10f}")
print(f"Riemann     = {r:.10f}   error = {r - exact:+.3e}")
print(f"Trapezoid   = {t:.10f}   error = {t - exact:+.3e}")
print(f"Simpson     = {s:.10f}   error = {s - exact:+.3e}")