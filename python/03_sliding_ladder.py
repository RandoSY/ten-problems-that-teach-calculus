"""Use the constraint x^2 + y^2 = L^2 to find the top's velocity."""
import numpy as np

from plot_support import BLUE, MUTED, RUST, TEAL, figure, options, save


def height(x, length):
    return np.sqrt(length**2 - x**2)


def main():
    args = options(__doc__)
    length, x0, foot_rate = 10.0, 6.0, 1.0
    y0 = height(x0, length)

    # PAPER: 2*x*dx/dt + 2*y*dy/dt = 0, so dy/dt = -(x/y)*dx/dt.
    # PYTHON: Evaluate the right-hand side at the requested position.
    top_rate = -(x0 / y0) * foot_rate

    # Independent check: move the foot over a tiny time interval centered at
    # the instant of interest. Recompute y from geometry at the two endpoints.
    dt = 1e-3
    check = (height(x0 + foot_rate * dt, length)
             - height(x0 - foot_rate * dt, length)) / (2 * dt)
    assert np.isclose(top_rate, check, rtol=1e-7)
    print(f"Ladder geometry: x = {x0:.1f} ft, y = {y0:.1f} ft, L = {length:.1f} ft.")
    print(f"Chain-rule prediction: {top_rate:+.4f} ft/s.")
    print(f"Centered finite-difference check: {check:+.8f} ft/s.")

    fig, (left, right) = figure(args, "03", "The sliding ladder")
    left.fill([0, x0, 0], [0, 0, y0], color=TEAL, alpha=0.1)
    left.plot([0, 0, 8.5], [9.2, 0, 0], color=MUTED, lw=1.5)
    left.plot([0, x0], [y0, 0], "o-", color=TEAL, lw=3, label="10 ft ladder")
    left.annotate("", xy=(0, 6.0), xytext=(0, 7.65),
                  arrowprops={"arrowstyle": "->", "color": RUST, "lw": 2})
    left.annotate("", xy=(8.0, 0), xytext=(6.3, 0),
                  arrowprops={"arrowstyle": "->", "color": BLUE, "lw": 2})
    left.text(1.40, 6.9, f"{top_rate:+.2f} ft/s", color=RUST)
    left.text(6.3, 0.43, f"{foot_rate:+.0f} ft/s", color=BLUE)
    left.set(xlim=(-0.8, 9.0), ylim=(-0.6, 9.4), aspect="equal",
             title="The geometry at the chosen instant", xlabel=r"Distance from wall $x$ (ft)",
             ylabel=r"Height $y$ (ft)")
    left.legend(loc="upper right")

    # x=L is excluded because the idealized derivative divides by y=0 there.
    x = np.linspace(0, 0.975 * length, 450)
    right.plot(x, -(x / height(x, length)) * foot_rate, color=TEAL, lw=2.3)
    right.scatter(x0, top_rate, color=RUST, zorder=5)
    right.axvline(x0, color=MUTED, ls=":", lw=1.2)
    right.annotate(f"({x0:.0f}, {top_rate:.2f})", (x0, top_rate), xytext=(12, 14),
                   textcoords="offset points", color=RUST)
    right.set(title="Top velocity depends on the position", xlabel=r"Foot position $x$ (ft)",
              ylabel=r"Top velocity $dy/dt$ (ft/s)")
    save(fig, args, "03_sliding_ladder")


if __name__ == "__main__":
    main()
