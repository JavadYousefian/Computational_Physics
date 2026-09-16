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


# Euler Explicit function 
def calc_euler_explicit(x_0, v_0, dt, N):
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

    # So it updated the list and get us x and v for steps number we have      
    return x, v


# Euler Symplectic function
def calc_euler_symplectic(x_0, v_0, dt, N):
    x = np.empty(N + 1)
    v = np.empty(N + 1)
    x[0] = x_0
    v[0] = v_0
    for i in range(N):
        v[i+1] = v[i] - (k / m) * x[i] * dt  

        # drift with new v
        x[i+1] = x[i] + v[i+1] * dt     

    # like the previous function, it updates the list and get us x and v for steps number we have       
    return x, v

def runge_kutta_second_order(x_0, v_0, dt, N):
    x = np.empty(N + 1)
    v = np.empty(N + 1)
    x[0] = x_0
    v[0] = v_0
    for i in range(N):
        # slope at start
        k1_x = v[i]
        k1_v = -(k / m) * x[i]
        # position and velocity at the midpoint
        x_m = x[i] + 0.5 * dt * k1_x
        v_m = v[i] + 0.5 * dt * k1_v
        # slope at midpoint
        k2_x = v_m
        k2_v = -(k / m) * x_m
        # full step using midpoint slope
        v[i+1] = v[i] + dt * k2_v
        x[i+1] = x[i] + dt * k2_x


    # Just get x and y updated based on second order runge kutta algorithm
    return x, v

# Force function
def calc_force(x = 0,v = 0, initial_t = 0):
    return (-k * x)

# Energy function
def energy(x, v):
    return 0.5 * m * v**2 + 0.5 * k * x**2

# Step size and total time
dt = 0.01
total_time = 60
step = int(total_time / dt)
t = np.linspace(0, step * dt, step + 1)

# Run each integrator
x1, v1 = calc_euler_explicit(x_0, v_0, dt, step)
x2, v2 = calc_euler_symplectic(x_0, v_0, dt, step)
x3, v3 = runge_kutta_second_order(x_0, v_0, dt, step)

# Exact solution for comparison for our oscillator
x_true = x_0 * np.cos(omega * t)

# plot x(t)
# note: I ran the code and when you zoom it is showing that exact and RK2 are nearly close rather than other methods
plt.figure(figsize=(10,4))
plt.plot(t, x_true, 'k--', label='exact', alpha=0.6)
plt.plot(t, x1, label='Euler explicit')
plt.plot(t, x2, label='Euler symplectic')
plt.plot(t, x3, label='Runge Kutta second_order')
plt.xlabel('t')
plt.ylabel('x(t)')
plt.title('position vs time')
plt.legend()
plt.savefig("Position vs Time.png")
plt.grid(alpha=0.3)
plt.show()


# Energy at each step for each method
# Using the functions I wrote for each method I get x and y and then put them in energy function to calc energy based on each method
E1 = energy(x1, v1)
E2 = energy(x2, v2)
E3 = energy(x3, v3)

# When I plotted RK2 stays close to E_0 (interesting)
plt.figure(figsize=(10,4))
plt.plot(t, E1, label='Euler explicit')
plt.plot(t, E2, label='Euler symplectic')
plt.plot(t, E3, label='RK2')
plt.axhline(E_0, color='k', ls='--', alpha=0.5, label='E_0')
plt.xlabel('t')
plt.ylabel('E(t)')
plt.title('energy vs time')
plt.legend()
plt.savefig("energy vs time.png")
plt.grid(alpha=0.3)
plt.show()

