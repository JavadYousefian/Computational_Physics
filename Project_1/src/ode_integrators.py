# Hand-written ODE integrators."""
import numpy as np


def euler_step(f, t, y, h):
    # One step of forward Euler method.
    #y_{n+1} = y_n + h * f(t_n, y_n)

    return y + h * f(t, y)



def integrate(f, t0, y0, t_end, h):
    # Integrate y' = f(t, y) from t0 to t_end with fixed step h.
    # Uses Euler method for now. Returns arrays of times and states.
    y0 = np.asarray(y0, dtype=float)
    n_steps = int(np.ceil((t_end - t0) / h))
    ts = np.empty(n_steps + 1)
    ys = np.empty((n_steps + 1, y0.size))
    ts[0] = t0
    ys[0] = y0

    t = t0
    y = y0.copy()
    for i in range(n_steps):
        y = euler_step(f, t, y, h)
        t = t + h
        ts[i + 1] = t
        ys[i + 1] = y

    return ts, ys