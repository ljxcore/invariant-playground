#!/usr/bin/env python3
"""Invariant Playground: numerical dynamics and residual diagnostics."""

import math

TAU = 2.0 * math.pi


def finite_number(value):
    """True only for finite real numeric values, excluding booleans."""
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
    )


class StateManifold:
    """Coordinate representation of M = S^1 x R."""

    @staticmethod
    def validate(state):
        return (
            isinstance(state, (tuple, list))
            and len(state) == 2
            and all(finite_number(v) for v in state)
        )

    @staticmethod
    def wrap(state):
        if not StateManifold.validate(state):
            raise ValueError("State must contain two finite coordinates.")
        theta, omega = state
        return ((theta + math.pi) % TAU - math.pi, omega)


def validate_parameters(p):
    required = ("g", "L", "m", "b")
    if not isinstance(p, dict) or any(k not in p for k in required):
        raise ValueError("Parameters must contain g, L, m, and b.")

    if not all(finite_number(p[k]) for k in required):
        raise ValueError("All physical parameters must be finite numbers.")

    if p["g"] <= 0 or p["L"] <= 0 or p["m"] <= 0:
        raise ValueError("g, L, and m must be positive.")

    if p["b"] < 0:
        raise ValueError("Damping coefficient b cannot be negative.")


def conservative(state, p):
    """Ideal pendulum vector field, with b = 0."""
    theta, omega = state
    return omega, -(p["g"] / p["L"]) * math.sin(theta)


def dissipative(state, p):
    """Damped pendulum vector field."""
    theta, omega = state
    return (
        omega,
        -(p["g"] / p["L"]) * math.sin(theta) - p["b"] * omega,
    )


def rk4_step(state, dt, field, p):
    """One classical fourth-order Runge-Kutta step."""
    if not StateManifold.validate(state):
        raise ValueError("State must contain two finite coordinates.")
    if not finite_number(dt) or dt <= 0:
        raise ValueError("dt must be finite and positive.")

    def add(s, k, scale):
        return s[0] + scale * k[0], s[1] + scale * k[1]

    k1 = field(state, p)
    k2 = field(add(state, k1, dt / 2), p)
    k3 = field(add(state, k2, dt / 2), p)
    k4 = field(add(state, k3, dt), p)

    result = tuple(
        state[i] + dt * (
            k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]
        ) / 6
        for i in range(2)
    )

    if not StateManifold.validate(result):
        raise FloatingPointError("Integrator produced a non-finite state.")

    # Angular wrapping is a coordinate change on S^1.
    return StateManifold.wrap(result)


def energy(state, p):
    """Mechanical energy of the ideal pendulum model."""
    theta, omega = state
    return (
        0.5 * p["m"] * p["L"]**2 * omega**2
        + p["m"] * p["g"] * p["L"] * (1 - math.cos(theta))
    )


def energy_rate(state, p, field):
    """Directional derivative dE/dt = grad(E) dot field(state)."""
    theta, omega = state
    theta_dot, omega_dot = field(state, p)

    dE_dtheta = p["m"] * p["g"] * p["L"] * math.sin(theta)
    dE_domega = p["m"] * p["L"]**2 * omega

    return dE_dtheta * theta_dot + dE_domega * omega_dot


def simulate(initial, p, field, dt, steps):
    validate_parameters(p)

    if not StateManifold.validate(initial):
        raise ValueError("Initial state must contain two finite coordinates.")
    if not finite_number(dt) or dt <= 0:
        raise ValueError("dt must be finite and positive.")
    if isinstance(steps, bool) or not isinstance(steps, int) or steps < 1:
        raise ValueError("steps must be a positive integer.")

    states = [StateManifold.wrap(initial)]

    for _ in range(steps):
        states.append(rk4_step(states[-1], dt, field, p))

    return states


def residuals(states, p):
    """Energy residual r_E(t) = E(x(t)) - E(x(0))."""
    if not states:
        raise ValueError("At least one state is required.")

    e0 = energy(states[0], p)
    return [energy(s, p) - e0 for s in states]


def diagnose(rs, dt, tolerance=1e-6):
    """
    Summarize residual behavior using explicit heuristic scores.

    Scores are descriptive, not probabilities, confidence estimates,
    or proofs of an invariant.
    """
    if len(rs) < 2 or not all(finite_number(r) for r in rs):
        raise ValueError("At least two finite residuals are required.")
    if not finite_number(dt) or dt <= 0:
        raise ValueError("dt must be finite and positive.")
    if not finite_number(tolerance) or tolerance <= 0:
        raise ValueError("tolerance must be finite and positive.")

    increments = [rs[i] - rs[i - 1] for i in range(1, len(rs))]
    net = rs[-1] - rs[0]
    max_abs = max(abs(r) for r in rs)

    negative_fraction = sum(d < 0 for d in increments) / len(increments)
    positive_fraction = sum(d > 0 for d in increments) / len(increments)

    if net < 0:
        monotone_fraction = negative_fraction
    elif net > 0:
        monotone_fraction = positive_fraction
    else:
        monotone_fraction = 0.0

    drift_score = (
        min(1.0, abs(net) / max(max_abs, 1e-300))
        * monotone_fraction
        if max_abs > 0 else 0.0
    )

    # This score is explicitly scaled to the caller's chosen tolerance.
    small_residual_score = 1.0 / (1.0 + max_abs / tolerance)

    if net < 0 and negative_fraction > 0.7:
        interpretation = "Predominantly decreasing energy residual."
    elif net > 0 and positive_fraction > 0.7:
        interpretation = "Predominantly increasing energy residual."
    else:
        interpretation = "No strong monotone residual-drift signature."

    return {
        "net_energy_change": net,
        "maximum_absolute_residual": max_abs,
        "negative_increment_fraction": negative_fraction,
        "positive_increment_fraction": positive_fraction,
        "drift_signature_score": drift_score,
        "small_residual_score": small_residual_score,
        "tolerance": tolerance,
        "interpretation": interpretation,
        "score_note": (
            "Heuristic scores, not calibrated probabilities. "
            "The small-residual score depends on the chosen tolerance."
        ),
    }


def run_case(name, field, p, initial, dt, steps):
    states = simulate(initial, p, field, dt, steps)
    rs = residuals(states, p)
    report = diagnose(rs, dt)

    print(f"\n--- {name} ---")
    print(f"Steps:                       {steps}")
    print(f"Duration:                    {dt * steps:.4f}")
    print(f"Initial energy:              {energy(states[0], p):.10f}")
    print(f"Final energy residual:       {rs[-1]:+.10e}")
    print(
        "Maximum absolute residual:   "
        f"{report['maximum_absolute_residual']:.10e}"
    )
    print(
        "Negative increment fraction: "
        f"{report['negative_increment_fraction']:.4f}"
    )
    print(f"Drift signature score:       {report['drift_signature_score']:.4f}")
    print(f"Small residual score:        {report['small_residual_score']:.4f}")
    print(f"Interpretation:              {report['interpretation']}")

    return report


def main():
    print("=" * 68)
    print("INVARIANT PLAYGROUND")
    print("State space: M = S^1 x R")
    print("Method: classical RK4")
    print("Diagnostic: mechanical-energy residual")
    print("=" * 68)

    common = {"g": 9.81, "L": 1.0, "m": 1.0}
    conservative_params = {**common, "b": 0.0}
    dissipative_params = {**common, "b": 0.08}

    initial = (1.2, 0.0)
    dt = 0.01
    steps = 1000

    conservative_report = run_case(
        "A: Conservative dynamics",
        conservative, conservative_params, initial, dt, steps
    )
    dissipative_report = run_case(
        "B: Dissipative dynamics",
        dissipative, dissipative_params, initial, dt, steps
    )

    print("\n--- Analytical energy-rate check ---")
    sample_state = (0.7, 1.3)
    rate_c = energy_rate(sample_state, conservative_params, conservative)
    rate_d = energy_rate(sample_state, dissipative_params, dissipative)
    expected_d = (
        -dissipative_params["b"]
        * dissipative_params["m"]
        * dissipative_params["L"]**2
        * sample_state[1]**2
    )

    print(f"Conservative dE/dt:          {rate_c:+.12e}")
    print(f"Dissipative dE/dt:           {rate_d:+.12e}")
    print(f"Analytical dissipative rate: {expected_d:+.12e}")
    print(
        "Dissipative identity:       ",
        "PASS" if math.isclose(rate_d, expected_d, rel_tol=1e-12, abs_tol=1e-12)
        else "FAIL"
    )

    print("\n--- Controlled comparison ---")
    print(
        "Conservative maximum residual: "
        f"{conservative_report['maximum_absolute_residual']:.10e}"
    )
    print(
        "Dissipative maximum residual:  "
        f"{dissipative_report['maximum_absolute_residual']:.10e}"
    )
    print(
        "Residual separation:           ",
        "PASS" if dissipative_report["maximum_absolute_residual"]
        > conservative_report["maximum_absolute_residual"] else "NOT ESTABLISHED"
    )
    print("\nThese are finite numerical results, not a general proof.")


if __name__ == "__main__":
    main()
