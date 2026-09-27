# main script for the ODE (coupled oscillator) part
# produces all figures needed for the report

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

from src.ode_integrators import integrate
from src.coupled_oscillator import rhs, exact_solution, energy


# where figures are saved
fig_dir = os.path.join("report", "figures")
os.makedirs(fig_dir, exist_ok=True)