"""Approximate exp(-0.1) by a quadratic and bound the error."""
import numpy as np

from plot_support import BLUE, RUST, TEAL, figure, options, save


def quadratic(x):
    # PAPER: f(0)=f'(0)=f''(0)=1. The coefficient of x^2 is 1/2!.
    return 1 + x + x**2 / 2


def remainder_bound(x):
    # On the interval between 0 and x, max exp(t) = exp(max(0, x)).
    # For the assigned x=-0.1, that maximum is 1.
    return np.exp(np.maximum(0, x)) * np.abs(x)**3 / 6


def main():
    args = options(__doc__)
    target = -0.1
    estimate = quadratic(target)

    # The exact library exponential is used only to check the approximation.
    reference = np.exp(target)
    error = abs(reference - estimate)
    bound = remainder_bound(target)
    assert reference < estimate and error < bound
    print(f"Taylor estimate at x={target:g}: {estimate:.9f}")
    print(f"Library exponential for comparison: {reference:.9f}")
    print(f"Absolute error: {error:.9f}")
    print(f"Guaranteed error bound: {bound:.9f}")

    fig, (left, right) = figure(args, "05", "Estimating an exponential")
    x = np.linspace(-0.65, 0.15, 350)
    left.plot(x, np.exp(x), color=TEAL, lw=2.4, label=r"$e^x$")
    left.plot(x, quadratic(x), "--", color=BLUE, lw=2, label=r"$P_2(x)=1+x+x^2/2$")
    left.scatter([target], [estimate], color=RUST, zorder=4, label="Target approximation")
    left.set(title="The curves agree closely near zero", xlabel=r"$x$", ylabel="Function value")
    left.legend(loc="upper left")

    x_near = np.linspace(-0.2, 0, 250)
    right.plot(x_near, 1000 * np.abs(np.exp(x_near) - quadratic(x_near)),
               color=TEAL, lw=2.5, label="Actual absolute error")
    right.plot(x_near, 1000 * remainder_bound(x_near), "--", color=BLUE, lw=1.9,
               label="Guaranteed upper bound")
    right.scatter([target], [1000 * error], color=RUST, zorder=5)
    right.annotate(f"Actual error\n{error:.7f}", (target, 1000 * error), xytext=(-12, 35),
                   textcoords="offset points", ha="center", color=RUST,
                   arrowprops={"arrowstyle": "->", "color": RUST})
    right.set(title="A close-up of what the quadratic leaves out", xlabel=r"$x$",
              ylabel=r"Absolute error ($\times\,10^{-3}$)")
    right.legend(loc="upper right")
    save(fig, args, "05_taylor_exponential")


if __name__ == "__main__":
    main()
