#!/usr/bin/env python3

from arena.report import print_header, print_result

def main():
    print_header()

    # Placeholder values until connected to the simulator.
    results = [
        ("Euler", 2.37e-2, 0.0009),
        ("Midpoint", 4.12e-4, 0.0018),
        ("RK4", 6.73e-8, 0.0031),
    ]

    results.sort(key=lambda x: x[1])

    for name, residual, runtime in results:
        print_result(name, residual, runtime)

    print()
    print("Winner:", results[0][0])

if __name__ == "__main__":
    main()
