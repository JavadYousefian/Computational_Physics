# main script for the integral (drag stopping distance) part
# produces all figures needed for the report

import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import trapezoid as scipy_trap
from scipy.integrate import simpson as scipy_simp

from src.quad_integrators import riemann, trapezoid, simpson
from src.drag_stopping import velocity, exact_distance, v0, tau


# where figures are saved
fig_dir = os.path.join("report", "figures")
os.makedirs(fig_dir, exist_ok=True)