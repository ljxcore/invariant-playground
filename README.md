# Invariant Playground

**An experimental numerical laboratory for exploring state manifolds, dynamical systems, conservation invariants, and residual-based diagnostics.**

---

## Overview

Most simulation software relies on brute-force numerical approximation, treating drift as an inevitable nuisance. **Invariant Playground** takes a structural approach: it models systems through formal state-manifold geometry and uses adaptive residual analysis to distinguish between numerical truncation error, unmodeled physical dissipation, and structural model breakdown.

Built with **zero external dependencies** (Python standard library only).

---

## Formal System Specification

$$\mathcal{S} = (M, T, \Phi, O, \mathcal{I})$$

* **$M$ (State Manifold):** Admissible state spaces with coordinate validation and topology wrapping (e.g., planar pendulum $M = S^1 \times \mathbb{R}$).
* **$T$ (Time Domain):** Continuous evolution via 4th-order Runge-Kutta (RK4) integration.
* **$\Phi$ (Evolution Operators):** Vector fields for conservative and dissipative systems.
* **$O$ (Observation Model):** Maps true states to measurements while tracking trajectory divergence.
* **$\mathcal{I}$ (Candidate Invariants):** Conserved quantities (e.g. total energy $E$) with residuals:

  $$r_Q(t) = Q(x(t)) - Q(x(0))$$

---

## Adaptive Residual Diagnostics

The diagnostic engine scores residual trajectories heuristically to rank likely causes:

1. **Numerical Integration Truncation:** Expected RK4 global convergence error.
2. **Unmodeled Physical Dissipation:** Monotonic damping signatures ($dE/dt < 0$).
3. **Structural Mismatch:** Anomalous behavior distinct from baseline noise.

---

## Quickstart

    python3 advanced_invariant_playground.py
