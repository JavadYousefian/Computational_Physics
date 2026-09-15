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

def euler_explicit(x_0, v_0, dt, N):
    x = np.empty(N + 1)
    v = np.empty(N + 1)
    x[0] = x_0
    v[0] = v_0
    for i in range(N):
        # force / mass
        a = -(k / m) * x[i] 
        # uses OLD v          
        x[i+1] = x[i] + v[i] * dt 
        # uses OLD x (through a)    
        v[i+1] = v[i] + a * dt        
    return x, v

# Force function
def calc_force(x, k):
    return (1/2 * k * (x**2))