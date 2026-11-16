"""Translate a definite integral into a sum of velocities times time widths."""
from fractions import Fraction

import numpy as np
from matplotlib.patches import Rectangle

from plot_support import BLUE, MUTED, RUST, TEAL, figure, options, save


def velocity(t):
    return t**2 - 1


def antiderivative(t):
    return t**3 / 3 - t


def midpoint_totals(n):
    # PAPER: Add v(t_i*) * Δt for displacement and |v(t_i*)| * Δt for distance.
    # PYTHON: Make n midpoints, evaluate the speeds, and add the contributions.
    dt = 2 / n
    t_mid = (np.arange(n) + 0.5) * dt
    changes = velocity(t_mid) * dt
    return changes.sum(), np.abs(changes).sum()


def main():
    args = options(__doc__)

    # Split at the direction change. Fractions keep these analytical values exact.
    start, turn, finish = map(Fraction, (0, 1, 2))
    backward = antiderivative(turn) - antiderivative(start)
    forward = antiderivative(finish) - antiderivative(turn)
    displacement = backward + forward
    distance = abs(backward) + abs(forward)

    # Odd slice counts let a rectangle straddle the turn. Both series
    # then show convergence. For this special velocity, even midpoint
    # counts happen to give the exact distance through cancellation.
    n_values = np.array([3, 5, 9, 17, 33, 65, 129, 257])
    numerical = np.array([midpoint_totals(n) for n in n_values])
    assert displacement == Fraction(2, 3) and distance == 2
    assert np.allclose(numerical[-1], [float(displacement), float(distance)], atol=1e-4)
    print(f"Backward leg: {backward} m. Forward leg: +{forward} m.")
    print(f"Exact displacement: {displacement} m. Exact distance: {distance} m.")
    print("Slices      Midpoint displacement (m)      Midpoint distance (m)")
    for n, (net, total) in zip(n_values, numerical):
        print(f"{n:>5d}             {net:.8f}                  {total:.8f}")

    fig, (left, right) = figure(args, "06", "How far did the cart travel?")
    t = np.linspace(0, 2, 401)
    v = velocity(t)
    left.fill_between(t, 0, v, where=(v < 0), color=RUST, alpha=0.20, label="Backward")
    left.fill_between(t, 0, v, where=(v >= 0), color=TEAL, alpha=0.21, label="Forward")
    left.plot(t, v, color=TEAL, lw=2, label=r"Velocity $t^2-1$")
    n_demo = 9
    dt = 2 / n_demo
    for i in range(n_demo):
        t_mid = (i + 0.5) * dt
        v_mid = velocity(t_mid)
        left.add_patch(Rectangle((i * dt, 0), dt, v_mid, fill=False, lw=1,
                                 edgecolor=MUTED, ls="--",
                                 label="Midpoint slices" if i == 0 else None))
    left.axhline(0, color=MUTED, lw=0.9)
    left.set(title="Velocity contributes signed area", xlabel="Time (s)", ylabel="Velocity (m/s)")
    left.legend(loc="upper left")

    right.plot(n_values, numerical[:, 0], "o-", color=BLUE, label="Riemann sum of velocity")
    right.plot(n_values, numerical[:, 1], "s-", color=TEAL, label="Riemann sum of speed")
    right.axhline(float(displacement), color=BLUE, ls="--", lw=1.1)
    right.axhline(float(distance), color=TEAL, ls="--", lw=1.1, label="Exact totals (dashed)")
    right.set_xscale("log", base=2)
    right.set_xticks(n_values, [str(n) for n in n_values])
    right.set(title="Two sums approach different totals", xlabel="Number of equal time slices",
              ylabel="Accumulated meters", ylim=(0.32, 2.32))
    right.legend(loc="center right")
    save(fig, args, "06_distance_vs_displacement")


if __name__ == "__main__":
    main()
