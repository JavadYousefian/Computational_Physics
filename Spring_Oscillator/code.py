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
E_0 = 0.5 * m * v_0 ** 2 + 0.5 * k * x_0 ** 2


# Force function (Hooke's law: F = -k*x)
# defined at the top so all integrators can use it to use acceleration 
def calc_force(x=0, v=0, initial_t=0):
    return (-k * x)


# Euler Explicit function
def calc_euler_explicit(x_0, v_0, dt, N):
    x = np.empty(N + 1)
    v = np.empty(N + 1)
    x[0] = x_0
    v[0] = v_0
    for i in range(N):
        # acceleration from calc_force (a = F/m)
        a = calc_force(x[i], v[i]) / m
        # uses old v
        x[i+1] = x[i] + v[i] * dt
        # uses old x (through a)
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
        a = calc_force(x[i], v[i]) / m
        v[i+1] = v[i] + a * dt

        x[i+1] = x[i] + v[i+1] * dt

    # like the previous function, it updates the list and get us x and v for steps number we have
    return x, v


# Second order Runge kutta
def runge_kutta_second_order(x_0, v_0, dt, N):
    x = np.empty(N + 1)
    v = np.empty(N + 1)
    x[0] = x_0
    v[0] = v_0
    for i in range(N):
        # slope at start (using calc_force)
        k1_x = v[i]
        k1_v = calc_force(x[i], v[i]) / m
        # position and velocity at the midpoint
        x_m = x[i] + 0.5 * dt * k1_x
        v_m = v[i] + 0.5 * dt * k1_v
        # slope at midpoint (using calc_force again, now at the midpoint state)
        k2_x = v_m
        k2_v = calc_force(x_m, v_m) / m
        # full step using midpoint slope
        v[i+1] = v[i] + dt * k2_v
        x[i+1] = x[i] + dt * k2_x

    # Just get x and y updated based on second order runge kutta algorithm
    return x, v

# Energy function
def energy(x, v):
    return 0.5 * m * v**2 + 0.5 * k * x**2

# Step size and total time to start comparing all three methods
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
plt.plot(t, E3, label='Runge Kutta second_order')
plt.axhline(E_0, color='k', ls='--', alpha=0.5, label='E_0')
plt.xlabel('t')
plt.ylabel('E(t)')
plt.title('energy vs time')
plt.legend()
plt.savefig("energy vs time.png")
plt.grid(alpha=0.3)
plt.show()

# try different time steps and see how the error changes
# i just put some times to check
time_steps = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.09, 0.1, 0.2, 0.3]
test_time = 20.0

# empty lists to store errors for each method
error_explicit = []
error_symplectic = []
error_rk2 = []

# loop over each time step
for dt_i in time_steps:
    num_steps = int(test_time / dt_i)

    # run each method
    x1, v1 = calc_euler_explicit(x_0, v_0, dt_i, num_steps)
    x2, v2 = calc_euler_symplectic(x_0, v_0, dt_i, num_steps)
    x3, v3 = runge_kutta_second_order(x_0, v_0, dt_i, num_steps)

    # get energy at the final step
    E_final_1 = energy(x1[-1], v1[-1])
    E_final_2 = energy(x2[-1], v2[-1])
    E_final_3 = energy(x3[-1], v3[-1])

    # relative error = |final energy - initial energy| / initial energy
    error_explicit.append(abs(E_final_1 - E_0) / E_0)
    error_symplectic.append(abs(E_final_2 - E_0) / E_0)
    error_rk2.append(abs(E_final_3 - E_0) / E_0)

# convert to arrays so we can plot reference lines easily
time_steps = np.array(time_steps)

# Plot on log-log scale
# After i plotted # both Eulers look like slope 1, so first order
# RK2 looks like slope 2, so second order
plt.figure(figsize=(8,6))
plt.loglog(time_steps, error_explicit, 'o-', label='Euler explicit')
plt.loglog(time_steps, error_symplectic, 's-', label='Euler symplectic')
plt.loglog(time_steps, error_rk2, '^-', label='Runge Kutta second_order')

plt.loglog(time_steps, time_steps, 'k:', alpha = 0.5, label='slope 1 (dt)')
plt.loglog(time_steps, time_steps ** 2, 'k--', alpha = 0.5, label='slope 2 (dt^2)')

plt.xlabel('dt')
plt.ylabel('relative energy error')
plt.title('error vs time step')
plt.legend()
plt.savefig("error vs time step.png")
plt.grid(alpha=0.3, which='both')
plt.show()


def modified_H(x, v, dt):
    return energy(x, v) - 0.5 * dt * k * x * v

# try a few different time steps to check
# the regular H wobbles with amplitude proportional to dt
# but H' is basically flat, so it's the conserved quantity
dt_list = [0.2, 0.1, 0.05]
run_time = 30.0

plt.figure(figsize=(10,5))

for dt_i in dt_list:
    num_steps = int(run_time / dt_i)
    t_i = np.linspace(0, num_steps * dt_i, num_steps + 1)

    # run symplectic Euler
    x, v = calc_euler_symplectic(x_0, v_0, dt_i, num_steps)

    # regular energy and modified energy
    H_regular = energy(x, v)
    H_prime = modified_H(x, v, dt_i)

    # plot deviation from E_0
    plt.plot(t_i, H_regular - E_0, alpha=0.4, label=f'H, dt={dt_i}')
    plt.plot(t_i, H_prime - E_0, label=f"H', dt={dt_i}")

plt.xlabel('t')
plt.ylabel('energy = E_0')
plt.title('regular vs modified Hamiltonian')
plt.legend(fontsize=8)
plt.grid(alpha=0.3)
plt.savefig("regular vs modified Hamiltonian.png")
plt.show()