"""
Reference numerical integrators.
"""

def euler_step(state, dt, field, params):
    dx = field(state, params)
    return (
        state[0] + dt * dx[0],
        state[1] + dt * dx[1],
    )


def midpoint_step(state, dt, field, params):
    k1 = field(state, params)

    mid = (
        state[0] + 0.5 * dt * k1[0],
        state[1] + 0.5 * dt * k1[1],
    )

    k2 = field(mid, params)

    return (
        state[0] + dt * k2[0],
        state[1] + dt * k2[1],
    )
