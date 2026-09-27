# Hand-written quadrature rules for definite integrals."""

import numpy as np


def riemann(f, a, b, n):
    # left Riemann sum
    # h * sum_{i=0}^{n-1} f(x_i),  x_i = a + i*h
    h = (b - a) / n
    xs = a + h * np.arange(n)   # left endpoints only
    return h * np.sum(f(xs))

def trapezoid(f, a, b, n):
    # trapezoidal rule
    # h * (f(x0)/2 + f(x1) + ... + f(x_{n-1}) + f(xn)/2)
    h = (b - a) / n
    xs = np.linspace(a, b, n + 1)
    ys = f(xs)
    return h * (0.5 * ys[0] + np.sum(ys[1:-1]) + 0.5 * ys[-1])