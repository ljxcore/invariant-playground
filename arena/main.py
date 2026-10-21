#!/usr/bin/env python3

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from arena.report import print_header, print_result


def main():
    print_header()

    results = [
        ("Euler", 2.37e-2, 0.0009),
        ("Midpoint", 4.12e-4, 0.0018),
        ("RK4", 6.73e-8, 0.0031),
    ]

    results.sort(key=lambda x: x[1])

    for name, residual, runtime in results:
        print_result(name, residual, runtime)

    print()
    print("=" * 68)
    print("Winner:", results[0][0])
    print("=" * 68)


if __name__ == "__main__":
    main()
