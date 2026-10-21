# Invariant Playground

A compact numerical laboratory for dynamical systems, candidate invariants,
and residual-based diagnostics. It uses Python's standard library only.

## State space and dynamics

The pendulum state is

    x = (theta, omega) in M = S^1 x R

where theta is angular position and omega is angular velocity.

The vector field is

    theta_dot = omega
    omega_dot = -(g/L) sin(theta) - b omega

The conservative model has b = 0. The dissipative model has b >= 0.

## Candidate invariant

The mechanical energy is

    E = (1/2) m L^2 omega^2 + mgL(1 - cos(theta))

For the conservative vector field, dE/dt = 0. For the dissipative
vector field,

    dE/dt = -b m L^2 omega^2 <= 0

These identities follow analytically from the equations. The simulation
tests whether the numerical results are consistent with them.

For a trajectory x(t), the energy residual is

    r_E(t) = E(x(t)) - E(x(0))

A small finite-time residual is numerical evidence, not proof of a general
invariant. RK4 has fourth-order global convergence under its usual
smoothness and stability assumptions; the test suite checks a finite-step
convergence ratio for this specific experiment.

## Diagnostics

The drift signature score summarizes the alignment of net residual change
with the direction of most residual increments. The small-residual score
is scaled to a declared tolerance. Neither is a calibrated probability,
confidence estimate, or proof of structure.

## Run

    python3 -m py_compile advanced_invariant_playground.py test_invariant_playground.py
    python3 -m unittest -v test_invariant_playground.py
    python3 advanced_invariant_playground.py

Python 3.9 or newer. No third-party packages required.
