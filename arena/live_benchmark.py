#!/usr/bin/env python3

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from benchmark.timer import benchmark
import advanced_invariant_playground as sim


def benchmark_rk4():
    params = {"g": 9.81, "L": 1.0, "m": 1.0, "b": 0.0}
    initial = (1.2, 0.0)

    states, runtime = benchmark(
        sim.simulate,
        initial,
        params,
        sim.conservative,
        0.01,
        1000,
    )

    residual = max(abs(r) for r in sim.residuals(states, params))

    return residual, runtime


def main():
    residual, runtime = benchmark_rk4()

    print("=" * 68)
    print("LIVE RK4 BENCHMARK")
    print("=" * 68)
    print(f"Maximum residual : {residual:.6e}")
    print(f"Runtime          : {runtime:.6f} s")


if __name__ == "__main__":
    main()
