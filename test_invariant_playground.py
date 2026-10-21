import math
import unittest

from advanced_invariant_playground import (
    StateManifold, conservative, dissipative, energy, energy_rate,
    simulate, residuals, diagnose
)


class InvariantPlaygroundTests(unittest.TestCase):
    def setUp(self):
        self.p = {"g": 9.81, "L": 1.0, "m": 1.0, "b": 0.08}
        self.pc = {**self.p, "b": 0.0}
        self.initial = (1.0, 0.0)

    def test_state_validation_and_angle_wrapping(self):
        self.assertTrue(StateManifold.validate((1.0, 2.0)))
        self.assertFalse(StateManifold.validate((math.nan, 2.0)))
        self.assertFalse(StateManifold.validate((1.0,)))
        theta, omega = StateManifold.wrap((7.0, 1.5))
        self.assertGreaterEqual(theta, -math.pi)
        self.assertLess(theta, math.pi)
        self.assertEqual(omega, 1.5)

    def test_energy_is_periodic_in_angle(self):
        a = (0.4, 2.0)
        b = (0.4 + 2 * math.pi, 2.0)
        self.assertAlmostEqual(energy(a, self.p), energy(b, self.p), places=12)

    def test_conservative_energy_drift_is_small(self):
        states = simulate(self.initial, self.pc, conservative, 0.01, 1000)
        rs = residuals(states, self.pc)
        self.assertLess(max(map(abs, rs)), 1e-5)

    def test_dissipative_energy_decreases(self):
        states = simulate(self.initial, self.p, dissipative, 0.01, 1000)
        rs = residuals(states, self.p)
        self.assertLess(rs[-1], 0.0)
        self.assertLess(energy(states[-1], self.p), energy(states[0], self.p))

    def test_analytical_energy_rate_identity(self):
        state = (0.7, 1.3)
        rate_c = energy_rate(state, self.pc, conservative)
        rate_d = energy_rate(state, self.p, dissipative)
        expected_d = -self.p["b"] * self.p["m"] * self.p["L"]**2 * state[1]**2
        self.assertAlmostEqual(rate_c, 0.0, places=12)
        self.assertAlmostEqual(rate_d, expected_d, places=12)

    def test_diagnostic_reports_signed_residual_behavior(self):
        report = diagnose([0.0, -0.01, -0.02], 0.01)
        self.assertAlmostEqual(report["maximum_absolute_residual"], 0.02)
        self.assertLess(report["net_energy_change"], 0)
        self.assertGreater(report["negative_increment_fraction"], 0.99)
        self.assertIn("decreasing", report["interpretation"].lower())

    def test_rk4_timestep_refinement(self):
        # Compare final states at the same time with a finer solution
        # as a reference. Wrapped angular distance respects S^1 geometry.
        duration = 5.0
        initial = (1.0, 0.0)

        coarse = simulate(initial, self.pc, conservative, 0.04, 125)[-1]
        medium = simulate(initial, self.pc, conservative, 0.02, 250)[-1]
        fine = simulate(initial, self.pc, conservative, 0.01, 500)[-1]

        def distance(a, b):
            dtheta = (a[0] - b[0] + math.pi) % (2 * math.pi) - math.pi
            return math.hypot(dtheta, a[1] - b[1])

        e_coarse = distance(coarse, fine)
        e_medium = distance(medium, fine)

        self.assertGreater(e_coarse, e_medium)
        ratio = e_coarse / max(e_medium, 1e-300)
        # The ideal asymptotic ratio is near 16; allow finite-step effects.
        self.assertGreater(ratio, 8.0, msg=f"Observed convergence ratio: {ratio}")
        self.assertLess(ratio, 25.0, msg=f"Observed convergence ratio: {ratio}")

    def test_invalid_inputs_are_rejected(self):
        with self.assertRaises(ValueError):
            simulate(self.initial, self.p, conservative, 0.0, 10)
        with self.assertRaises(ValueError):
            simulate(self.initial, self.p, conservative, 0.01, 0)
        with self.assertRaises(ValueError):
            simulate(self.initial, {**self.p, "b": -1}, dissipative, 0.01, 10)


if __name__ == "__main__":
    unittest.main()
