#!/usr/bin/env python3

from benchmark.timer import benchmark
import advanced_invariant_playground as sim


def benchmark_rk4():
    common = {"g": 9.81, "L": 1.0, "m": 1.0, "b": 0.0}
    initial = (1.2, 0.0)

    _, elapsed = benchmark(
        sim.simulate,
        initial,
        common,
        sim.conservative,
        0.01,
        1000,
    )

    states = sim.simulate(
        initial,
        common,
        sim.conservative,
        0.01,
        1000,
    )

    residual = max(abs(r) for r in sim.residuals(states, common))

    return residual, elapsed


if __name__ == "__main__":
    residual, runtime = benchmark_rk4()

    print("=" * 68)
    print("LIVE RK4 BENCHMARK")
    print("=" * 68)
    print(f"Maximum residual : {residual:.6e}")
    print(f"Runtime          : {runtime:.6f} s")
