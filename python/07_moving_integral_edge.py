"""Differentiate a moving-endpoint integral without finding an antiderivative."""
import numpy as np

from plot_support import BLUE, MUTED, RUST, TEAL, figure, options, save


def integrand(t):
    return np.cos(t**2)


def edge(x):
    return x**2


def area_slope(x):
    # PAPER: FTC gives the height at the edge. Chain rule supplies edge speed.
    # PYTHON: Evaluate cos(t^2) at t=x^2, then multiply by 2*x.
    return integrand(edge(x)) * 2 * x


def area(x, slices=2500):
    # Midpoint estimate of A(x). Used only for the numerical check of A'(x).
    width = edge(x) / slices
    t_mid = (np.arange(slices) + 0.5) * width
    return integrand(t_mid).sum() * width


def main():
    args = options(__doc__)
    x0 = 0.9
    exact_slope = area_slope(x0)
    h = 1e-4
    finite_difference = (area(x0 + h) - area(x0 - h)) / (2 * h)
    assert np.isclose(exact_slope, finite_difference, rtol=2e-6)
    print(f"At x={x0:.2f}, the edge is x^2={edge(x0):.4f} and moves at {2*x0:.4f}.")
    print(f"Integrand at the edge: {integrand(edge(x0)):.8f}")
    print(f"FTC and chain-rule derivative: {exact_slope:.8f}")
    print(f"Centered difference of numerical areas: {finite_difference:.8f}")

    fig, (left, right) = figure(args, "07", "The moving edge of an integral")
    # An exaggerated step makes the small added strip visible.
    dx_visible = 0.10
    old, new = edge(x0), edge(x0 + dx_visible)
    t = np.linspace(0, 1.42, 350)
    t_before = np.linspace(0, old, 200)
    t_added = np.linspace(old, new, 100)
    left.plot(t, integrand(t), color=TEAL, lw=2, label=r"Integrand $\cos(t^2)$")
    left.fill_between(t_before, 0, integrand(t_before), color=BLUE, alpha=0.18, label="Existing area")
    left.fill_between(t_added, 0, integrand(t_added), color=RUST, alpha=0.34, label="Area added")
    for a in (old, new):
        left.axvline(a, color=MUTED, lw=1, ls=":")
    left.axhline(0, color=MUTED, lw=0.8)
    left.set(title="Increasing x moves the upper edge",
             xlabel=r"Integration variable $t$", ylabel="Height", ylim=(-0.54, 1.28))
    left.legend(loc="lower left")

    x = np.linspace(-1.35, 1.35, 350)
    probes = np.linspace(-1.3, 1.3, 15)
    differences = [(area(q+h) - area(q-h)) / (2*h) for q in probes]
    assert np.max(np.abs(area_slope(probes)-differences)) < 2e-6
    right.plot(x, area_slope(x), color=TEAL, lw=2.2, label=r"Analytical $A'(x)=2x\cos(x^4)$")
    right.scatter(probes, differences, fc="white", ec=BLUE, s=31, zorder=4,
                  label="Finite differences of numerical areas")
    right.scatter([x0], [exact_slope], color=RUST, s=58, zorder=5, label=r"At $x=0.9$")
    right.axhline(0, color=MUTED, lw=0.8)
    right.set(title="Edge height × edge speed", xlabel=r"$x$", ylabel=r"Rate of change $A'(x)$",
              ylim=(-3.1, 3.1))
    right.legend(loc="upper center")
    save(fig, args, "07_moving_integral_edge")


if __name__ == "__main__":
    main()
