"""
AI Analysis module for Invariant Playground.
Converts numerical diagnostics into a human-readable report.
"""

def generate_report(results):
    lines = []

    lines.append("=" * 60)
    lines.append("AI ANALYSIS REPORT")
    lines.append("=" * 60)
    lines.append("")

    c = results["conservative_max_residual"]
    d = results["dissipative_max_residual"]

    lines.append("Simulation Health")
    lines.append("-----------------")

    if c < 1e-6:
        lines.append("✓ Conservative simulation is numerically stable.")
    else:
        lines.append("! Conservative residual exceeded nominal tolerance.")

    if results["identity_pass"]:
        lines.append("✓ Analytical energy identity verified.")
    else:
        lines.append("! Analytical energy identity failed.")

    lines.append("")

    lines.append("Scientific Interpretation")
    lines.append("-------------------------")

    if d > c * 1000:
        lines.append("The dissipative model exhibits significantly greater")
        lines.append("energy loss than the conservative model, consistent")
        lines.append("with physical damping.")
    else:
        lines.append("The two models are not well separated.")

    lines.append("")

    lines.append("Metrics")
    lines.append("-------")
    lines.append(f"Conservative residual : {c:.3e}")
    lines.append(f"Dissipative residual  : {d:.3e}")

    lines.append("")

    lines.append("AI Recommendation")
    lines.append("-----------------")
    lines.append("• Compare additional numerical integrators.")
    lines.append("• Add a chaotic dynamical system.")
    lines.append("• Export a Markdown experiment report.")

    return "\n".join(lines)
