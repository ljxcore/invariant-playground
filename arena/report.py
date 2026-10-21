def print_header():
    print()
    print("=" * 68)
    print("INTEGRATOR ARENA")
    print("=" * 68)
    print(f'{"Method":<15}{"Residual":<20}{"Runtime (s)"}')
    print("-" * 68)


def print_result(name, residual, runtime):
    print(f"{name:<15}{residual:<20.3e}{runtime:.6f}")
