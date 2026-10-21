"""
Integrator Arena experiment.
"""

from integrators.basic import euler_step, midpoint_step

INTEGRATORS = {
    "Euler": euler_step,
    "Midpoint": midpoint_step,
    "RK4": None,   # Filled by the main engine.
}
