# Quick test: run Euler on the coupled oscillator and print first few steps.

import numpy as np
from src.ode_integrators import integrate
from src.coupled_oscillator import rhs


# initial condition: x1 = 1, x2 = 0, both at rest
y0 = np.array([1.0, 0.0, 0.0, 0.0])

# integrate from t=0 to t=2 with step h=0.1
ts, ys = integrate(rhs, 0.0, y0, 2.0, 0.1)

# print first few time steps
print("time     x1        x2")
for i in range(5):
    print(f"{ts[i]:.2f}   {ys[i, 0]:+.4f}   {ys[i, 1]:+.4f}")