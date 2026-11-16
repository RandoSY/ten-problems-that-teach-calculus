"""Estimate the velocity at t=3 from average rates on either side."""
import numpy as np

from plot_support import BLUE, MUTED, RUST, TEAL, figure, options, save


def position(t):
    return t**2


def average_velocity(t0, h):
    if np.any(np.asarray(h) == 0):
        raise ValueError("The difference quotient requires h != 0.")
    return (position(t0 + h) - position(t0)) / h


def main():
    args = options(__doc__)
    t0 = 3.0

    # PAPER: Expand (3+h)^2 - 9 to get h*(6+h); cancel h before taking the limit.
    # PYTHON: Compute the original quotient and compare to the simplified one.
    h = np.array([-0.8, -0.1, -0.01, 0.01, 0.1, 0.8])
    measured = average_velocity(t0, h)
    simplified = 6 + h
    assert np.allclose(measured, simplified, rtol=0, atol=1e-11)
    limit = 6.0
    print("h (s)      difference quotient        6 + h")
    for offset, q, s in zip(h, measured, simplified):
        print(f"{offset:+.2f}           {q:.5f}            {s:.5f}")
    print(f"Instantaneous velocity: {limit:.2f} m/s. The code never divides by zero.")

    fig, (left, right) = figure(args, "02", "Speed at one instant")
    t = np.linspace(2.05, 3.95, 300)
    left.plot(t, position(t), color=TEAL, lw=2.3, label=r"Position $s(t)=t^2$")
    left.plot(t, position(t0) + limit * (t - t0), "--", color=MUTED, label="Tangent at 3 s")
    for offset, color in [(-0.8, BLUE), (0.8, RUST)]:
        t_pair = np.array([t0, t0 + offset])
        left.plot(t_pair, position(t_pair), "o-", color=color, lw=2, label=f"Secant h={offset:+.1f} s")
    left.set(title="Secant slopes approach a tangent slope", xlabel="Time (s)", ylabel="Position (m)")
    left.legend(loc="upper left")

    h_curve = np.linspace(-0.85, 0.85, 300)
    right.plot(h_curve, 6 + h_curve, color=TEAL, lw=2, label=r"Simplified slope $6+h$")
    right.scatter(h, measured, color=BLUE, s=26, zorder=3, label="Evaluated quotient")
    right.scatter([0], [limit], facecolors="white", edgecolors=RUST, s=110,
                  linewidths=2, zorder=5, label="Limit (quotient undefined at 0)")
    right.set(title="The two sides agree", xlabel=r"Time offset $h$ (s)", ylabel="Average velocity (m/s)")
    right.legend(loc="upper left")
    save(fig, args, "02_instantaneous_velocity")


if __name__ == "__main__":
    main()
