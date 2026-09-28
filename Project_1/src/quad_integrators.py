# Hand-written quadrature rules for definite integrals.
# All three rules approximate integral from a to b of f(x) dx.
# I divide [a,b] into n sub-intervals of width h = (b-a)/n.

import numpy as np

# Reiemann is asked in the project 1
# Equation 5 in my plan 
def riemann(f, a, b, n):
    # Left Riemann sum: approximate the area under f by rectangles.
    # For each sub-interval, use the value of f at the LEFT endpoint
    # as the height of the rectangle. Then add up n rectangles.
    # Formula: h * sum_{i=0}^{n-1} f(x_i),  with x_i = a + i*h
    # This is the simplest rule -> also the least accurate (only 1st order).
    h = (b - a) / n
    xs = a + h * np.arange(n)   # left endpoints x_0, x_1, ..., x_{n-1}
    return h * np.sum(f(xs))

# Trapezoidal rule as it is asked 
def trapezoid(f, a, b, n):
    # Trapezoidal rule: approximate f by a straight line on each sub-interval,
    # not by a flat rectangle. So each sub-interval area is a trapezoid,
    # (h/2) * (f(x_i) + f(x_{i+1})).
    # Adding them up, the interior points get counted twice, so:
    #   h * (f(x_0)/2 + f(x_1) + ... + f(x_{n-1}) + f(x_n)/2)
    # More accurate than Riemann (2nd order).
    h = (b - a) / n
    xs = np.linspace(a, b, n + 1)   # all endpoints including both ends
    ys = f(xs)
    return h * (0.5 * ys[0] + np.sum(ys[1:-1]) + 0.5 * ys[-1])

# Simpson as it is asked
def simpson(f, a, b, n):
    # Simpson's 1/3 rule: approximate f by a parabola across every 2
    # sub-intervals (so it takes 3 points to fit each parabola).
    # This is why n must be even.
    
    # The rule can be written as:
    #   (h/3) * [f(x_0) + f(x_n) + 4*sum(f at odd indices) + 2*sum(f at even interior indices)]
    # Much more accurate than the other two (4th order) because it also
    # gets cubic functions exactly, not just parabolas.
    if n % 2 != 0:
        raise ValueError("Simpson needs even n")
    h = (b - a) / n
    xs = np.linspace(a, b, n + 1)
    ys = f(xs)
    return (h / 3.0) * (ys[0] + ys[-1] + 4.0 * np.sum(ys[1:-1:2]) + 2.0 * np.sum(ys[2:-1:2]))