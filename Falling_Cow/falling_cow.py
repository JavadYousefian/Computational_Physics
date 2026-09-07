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
def get_force(x_0, y_0, v_x, v_y, mass, drag):

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




