Javad Yousefian
# Project 1 — Coupled Oscillator (ODE) and Stopping-Distance (Integral)

Numerical integrators for two classical-mechanics problems, both of which have exact closed form solutions. The ODE problem is a two mass, three spring coupled oscillator. The definite integral problem is the distance travelled by an object slowing under linear drag.


## Install
Needs Python 3 with numpy, scipy, and matplotlib. Install with:

    pip install -r requirements.txt

## Run
Two main scripts, one for each problem:

    python main_ode.py
    python main_integral.py

## Files

- `main_ode.py` — runs all experiments for the coupled oscillator
- `main_integral.py` — runs all experiments for the drag stopping distance
- `src/coupled_oscillator.py` — physics of the two-mass oscillator (RHS, exact solution, energy)
- `src/drag_stopping.py` — physics of the drag problem (velocity, exact distance)
- `src/ode_integrators.py` — Euler and RK4 written by hand
- `src/quad_integrators.py` — Riemann, trapezoid, Simpson written by hand
- `report/report.pdf` — Report write-up (I used LATEX and converted to PDF)
- `figures/` — figures made by the main scripts
- `plan/` - Plan for my project that i wanted to do
