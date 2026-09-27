# Physics for the two-mass, three-spring coupled oscillator.
# Setup: wall - m1 - (spring) - m2 - wall, all three springs identical.

import numpy as np


# physical parameters
m = 1.0   # mass of each block
k = 1.0   # spring constant (same for all three springs)


def rhs(t, y):
    # right-hand side of the ODE system
    # state vector: y = (x1, x2, v1, v2)
    #
    # How I got the equations of motion:
    # The left spring pulls mass 1 back with force -k*x1.
    # The middle spring is stretched by (x2 - x1), so it pulls
    # mass 1 with force +k*(x2 - x1) and mass 2 with the opposite -k*(x2 - x1).
    # The right spring pulls mass 2 back with force -k*x2.
    #
    # Newton's second law then gives:
    #   m*x1'' = -k*x1 + k*(x2 - x1) = -2*k*x1 + k*x2
    #   m*x2'' = -k*(x2 - x1) - k*x2 = k*x1 - 2*k*x2
    #
    # These are 2nd order but I need a 1st order system for the integrator,
    # so I use v1 = x1', v2 = x2' and split into 4 first-order equations.
    x1, x2, v1, v2 = y
    a1 = (-2.0 * k * x1 + k * x2) / m
    a2 = (k * x1 - 2.0 * k * x2) / m
    return np.array([v1, v2, a1, a2])


# normal-mode angular frequencies
# To find them I try x1, x2 ~ exp(i*omega*t) in the equations of motion,
# which turns the system into a 2x2 eigenvalue problem. Solving gives:
#   omega_plus  = sqrt(k/m)     in-phase mode   (x1 = x2)
#   omega_minus = sqrt(3*k/m)   out-of-phase mode (x1 = -x2)
#
# In the in-phase mode both masses move together, so the middle spring
# is never stretched -> only outer springs contribute -> lower frequency.
# In the out-of-phase mode the middle spring is stretched twice as much,
# so the effective stiffness is bigger -> higher frequency (factor sqrt(3)).
omega_plus = np.sqrt(k / m)
omega_minus = np.sqrt(3 * k / m)


def exact_solution(t, y0):
    # Any initial condition is a combination of the two normal modes.
    # Each mode oscillates independently at its own frequency, so:
    #   1) project (x1, x2, v1, v2) at t=0 onto mode coordinates q+ and q-
    #   2) evolve each mode with cos and sin (harmonic oscillator solution)
    #   3) rotate back to (x1, x2, v1, v2)
    #
    # Mode coordinates:
    #   q+ = (x1 + x2) / sqrt(2)   in-phase amplitude
    #   q- = (x1 - x2) / sqrt(2)   out-of-phase amplitude
    t = np.asarray(t, dtype=float)
    x1_0, x2_0, v1_0, v2_0 = y0

    # step 1: project onto normal-mode coordinates at t = 0
    q_plus_0 = (x1_0 + x2_0) / np.sqrt(2.0)
    q_minus_0 = (x1_0 - x2_0) / np.sqrt(2.0)
    p_plus_0 = (v1_0 + v2_0) / np.sqrt(2.0)
    p_minus_0 = (v1_0 - v2_0) / np.sqrt(2.0)

    # step 2: evolve each mode as a simple harmonic oscillator
    q_plus = q_plus_0 * np.cos(omega_plus * t) + (p_plus_0 / omega_plus) * np.sin(omega_plus * t)
    q_minus = q_minus_0 * np.cos(omega_minus * t) + (p_minus_0 / omega_minus) * np.sin(omega_minus * t)
    p_plus = -q_plus_0 * omega_plus * np.sin(omega_plus * t) + p_plus_0 * np.cos(omega_plus * t)
    p_minus = -q_minus_0 * omega_minus * np.sin(omega_minus * t) + p_minus_0 * np.cos(omega_minus * t)

    # step 3: rotate back to (x1, x2, v1, v2)
    x1 = (q_plus + q_minus) / np.sqrt(2.0)
    x2 = (q_plus - q_minus) / np.sqrt(2.0)
    v1 = (p_plus + p_minus) / np.sqrt(2.0)
    v2 = (p_plus - p_minus) / np.sqrt(2.0)

    return np.stack([x1, x2, v1, v2], axis=-1)


def energy(y):
    # total mechanical energy = kinetic + potential
    #
    # Kinetic: (1/2)*m*v^2 for each mass, added.
    # Potential: (1/2)*k*(stretch)^2 for each of the three springs.
    #   left spring stretch    = x1
    #   middle spring stretch  = x2 - x1
    #   right spring stretch   = x2
    #
    # No friction anywhere, so E(t) should be constant. Any change I see
    # in E(t) is coming from the numerical method, not physics.
    y = np.asarray(y)
    x1 = y[..., 0]
    x2 = y[..., 1]
    v1 = y[..., 2]
    v2 = y[..., 3]
    KE = 0.5 * m * (v1**2 + v2**2)
    PE = 0.5 * k * (x1**2 + (x2 - x1)**2 + x2**2)
    return KE + PE