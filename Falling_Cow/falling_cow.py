# Importing Packages
import math
import matplotlib.pyplot as plt


# Initial Conditions
v_x = 1
v_y = 100
drag = 0
x_0 = 0
y_0 = 1000
time_step = 0.001
t = 0
mass = 1000
g = 9.8

# Force Function
def calc_force(x_0, y_0, v_x, v_y, mass, drag):

    f_x = 0
    f_y = - mass * g

    speed = math.sqrt(v_x**2 + v_y**2)
    f_x = f_x - drag * speed * v_x
    f_y = f_y - drag * speed * v_y

    return f_x, f_y

# Velocity Function
def update_velocity(v_x, v_y, f_x, f_y, mass, time_step):

    a_x = f_x / mass
    a_y = f_y / mass

    new_v_x = v_x + a_x * time_step
    new_v_y = v_y + a_y * time_step

    return new_v_x, new_v_y

# Position Function
def update_position(x_0, y_0, v_x, v_y, time_step):

    new_x = x_0 + v_x * time_step
    new_y = y_0 + v_y * time_step

    return new_x, new_y


# Energy Function
def calc_energy(x_0, y_0, v_x, v_y, mass):

    Kinetic_energy = 0.5 * mass * (v_x**2 + v_y**2)
    Potential_energy = mass * g * y_0
    Total_energy = Kinetic_energy + Potential_energy

    return Kinetic_energy, Potential_energy, Total_energy

# Empty lists to save everything
times = []
x_all = []
y_all = []
v_x_all = []
v_y_all = []
KE_all = []
PE_all = []
total_all = []

# Until it reaches the ground the loop continues and starts from 1000 we set at initial variables
while y_0 > 0:

    times.append(t)
    x_all.append(x_0)
    y_all.append(y_0)
    v_x_all.append(v_x)
    v_y_all.append(v_y)

    Kinetic_energy, Potential_energy, Total_energy = calc_energy(x_0, y_0, v_x, v_y, mass)
    KE_all.append(Kinetic_energy)
    PE_all.append(Potential_energy)
    total_all.append(Total_energy)

    f_x, f_y = calc_force(x_0, y_0, v_x, v_y, mass, drag)

    v_x, v_y = update_velocity(v_x, v_y, f_x, f_y, mass, time_step)
    x_0, y_0 = update_position(x_0, y_0, v_x, v_y, time_step)

    t = t + time_step

