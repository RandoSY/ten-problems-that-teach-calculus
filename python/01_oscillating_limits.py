"""Compare sin(1/x) and x*sin(1/x) near zero (PDF problem 01)."""
import numpy as np

from plot_support import BLUE, INK, MUTED, RUST, TEAL, figure, options, save


def main():
    args = options(__doc__)

    # PAPER: Approach x=0 along two sequences with sine values +1 and -1.
    # PYTHON: Construct the exact phases first, then invert them.
    n = np.arange(1, 7)
    x_plus = 1 / (np.pi / 2 + 2 * np.pi * n)
    x_minus = 1 / (3 * np.pi / 2 + 2 * np.pi * n)
    y_plus = np.sin(1 / x_plus)
    y_minus = np.sin(1 / x_minus)
    assert np.allclose(y_plus, 1) and np.allclose(y_minus, -1)

    # Plot by uniform steps in phase, not in x. This gives every cycle enough
    # samples. Stop at a finite phase. No plot can show all the oscillations.
    phase = np.linspace(5, 135, 4000)
    x = 1 / phase
    y = np.sin(phase)

    # PAPER: |x*sin(1/x)| <= |x|. Check the inequality on the plotted samples.
    squeezed = x * y
    assert np.all(np.abs(squeezed) <= x + 1e-15)
    print("n      x_plus       sin(1/x_plus)      x_minus      sin(1/x_minus)")
    for k, a, b, ya, yb in zip(n, x_plus, x_minus, y_plus, y_minus):
        print(f"{k:1d}      {a:.6f}         {ya:+.0f}             {b:.6f}          {yb:+.0f}")
    print("The two sequences disagree. For x*sin(1/x), the envelope -> 0.")
    print("The plot shows x > 0. The paper's squeeze bound holds on both sides.")

    fig, (left, right) = figure(args, "01", "Oscillating near zero")
    left.plot(x, y, color=TEAL, lw=1.4)
    left.scatter(x_plus, y_plus, color=BLUE, s=32, label=r"$\sin(1/x_n)=1$", zorder=4)
    left.scatter(x_minus, y_minus, color=RUST, s=32, marker="s",
                 label=r"$\sin(1/y_n)=-1$", zorder=4)
    left.set(title="Two sequences, two different values", xlabel=r"$x$ (right of zero)",
             ylabel=r"$\sin(1/x)$", ylim=(-1.4, 1.4))
    left.legend(loc="upper right", ncol=2)

    envelope_x = np.linspace(0, 0.20, 200)
    right.fill_between(envelope_x, -envelope_x, envelope_x, color=TEAL, alpha=0.09)
    right.plot(envelope_x, envelope_x, "--", color=MUTED, lw=1.3, label=r"$\pm x$ for $x>0$")
    right.plot(envelope_x, -envelope_x, "--", color=MUTED, lw=1.3)
    right.plot(x, squeezed, color=TEAL, lw=1.5, label=r"$x\sin(1/x)$")
    right.scatter([0], [0], color=INK, s=40, zorder=4, label="Continuous extension")
    right.set(title="The envelope shrinks to zero", xlabel=r"$x$ (right of zero)",
              ylabel=r"$x\sin(1/x)$", ylim=(-0.23, 0.23))
    right.legend(loc="upper left")
    for ax in (left, right):
        ax.set_xlim(-0.004, 0.204)
        ax.axhline(0, color=MUTED, lw=0.75)
    save(fig, args, "01_oscillating_limits")


if __name__ == "__main__":
    main()
