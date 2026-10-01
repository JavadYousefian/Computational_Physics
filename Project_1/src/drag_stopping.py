# Physics for the linear drag stopping distance problem.
# This part is for part b or integral of my plan
# An object with initial speed v0 slows down under a drag force F = -b*v.
# Solving Newton's second law m*v' = -b*v by separating variables gives:
# dv/v = -(b/m) dt
# ln(v) = -(b/m)*t + const
# and using v(0) = v0:
# v(t) = v0 * exp(-t/tau),  where tau = m/b
# tau is the time it takes for the speed to drop by a factor of e.

# Like before, import the packages I need
import numpy as np


# physical parameters
v0 = 1.0    # initial speed
tau = 1.0   # time constant = m / b

# Equation 4 in my plan
def velocity(t):
    # v(t) = v0 * exp(-t/tau)
    # This is what I need to integrate to get the distance travelled.
    # (formula 4 in my plan)
    return v0 * np.exp(-np.asarray(t) / tau)

# Equations 5 and 6 in my plan
def exact_distance(T):
    # x(T) = integral from 0 to T of v(t) dt = integral from 0 to T of v0*exp(-t/tau) dt
    # Doing the integral by hand (antiderivative is -v0*tau*exp(-t/tau)):
    # x(T) = v0*tau*(1 - exp(-T/tau))
    # This is the "exact" answer I compare my Riemann/Trapezoid/Simpson to.
    return v0 * tau * (1.0 - np.exp(-T / tau))