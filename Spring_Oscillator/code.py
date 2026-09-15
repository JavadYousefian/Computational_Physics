# Importing libraries
import numpy as np
import matplotlib.pyplot as plt

# Initial conditions:
# spring constant, mass, angular frequency
k = 1.0
m = 1.0
omega = np.sqrt(k / m)

# initial condition: pulled to x=1, released from rest
x_0 = 1.0
v_0 = 0.0

# initial energy (for comparison later)
E_0 = 0.5 * m * v_0**2 + 0.5 * k * x_0**2