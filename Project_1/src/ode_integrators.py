# Hand-written ODE integrators.
# Two methods: forward Euler (simple, 1st order) and RK4 (fancier, 4th order).

import numpy as np


def euler_step(f, t, y, h):
    # One step of forward Euler.
    
    # Where it comes from: Taylor expansion of y(t+h) around t is
    #   y(t + h) = y(t) + h*y'(t) + (h^2/2)*y''(t) + ...
    # Euler keeps only the first two terms and drops the rest.
    # So the update rule is:
    #   y_{n+1} = y_n + h * f(t_n, y_n)
    # where f = y' is the RHS I'm integrating.
    return y + h * f(t, y)


def rk4_step(f, t, y, h):
    # One step of classical 4th-order Runge-Kutta.
    # Way more accurate than Euler because it uses 4 slope estimates
    # inside one step instead of just 1:
    #   k1 = slope at the start
    #   k2 = slope at the midpoint using k1 to get there
    #   k3 = slope at the midpoint again but using k2
    #   k4 = slope at the end using k3
    # Then combine them with weights (1, 2, 2, 1)/6 which is the standard
    k1 = f(t, y)
    k2 = f(t + 0.5 * h, y + 0.5 * h * k1)
    k3 = f(t + 0.5 * h, y + 0.5 * h * k2)
    k4 = f(t + h, y + h * k3)
    return y + (h / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

# This is ODE integrator by hand
def integrate(f, t0, y0, t_end, h, method="rk4"):
    # Integrate y' = f(t, y) from t0 to t_end with fixed step h.
    # Choose method with method="euler" or method="rk4".
    # Returns arrays of times and states.

    # pick which step function to use
    if method == "euler":
        step = euler_step
    elif method == "rk4":
        step = rk4_step
    else:
        raise ValueError("Unknown method: " + method)

    # allocate arrays for the result
    y0 = np.asarray(y0, dtype=float)
    n_steps = int(np.ceil((t_end - t0) / h))
    ts = np.empty(n_steps + 1)
    ys = np.empty((n_steps + 1, y0.size))
    ts[0] = t0
    ys[0] = y0

    # main integration loop: keep stepping until we reach t_end
    t = t0
    y = y0.copy()
    for i in range(n_steps):
        y = step(f, t, y, h)
        t = t + h
        ts[i + 1] = t
        ys[i + 1] = y

    return ts, ys