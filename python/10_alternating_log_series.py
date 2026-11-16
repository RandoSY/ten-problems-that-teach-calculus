"""Turn the exact remainder of the alternating log series into a stopping rule."""
from fractions import Fraction
from math import log

import numpy as np

from plot_support import BLUE, MUTED, RUST, TEAL, figure, options, save


def exact_error_bounds(n):
    # PAPER: E_N = ∫_0^1 x^N/(1+x) dx. For 0<x<1:
    # 1/2 < 1/(1+x) < 1-x/2. Integrating gives strict lower/upper bounds.
    lower = Fraction(1, 2 * (n + 1))
    upper = Fraction(1, n + 1) - Fraction(1, 2 * (n + 2))
    return lower, upper


def first_certified_count(tolerance):
    # RECIPE: Increase N until the strict upper bound <= the target.
    # Then use the strict lower bound at N-1 to test whether it is minimal.
    n = 1
    while exact_error_bounds(n)[1] > tolerance:
        n += 1
    return n


def main():
    args = options(__doc__)
    tol = Fraction(1, 1000)
    n_certified = first_certified_count(tol)
    lower_at_previous, _ = exact_error_bounds(n_certified - 1)
    _, upper_at_certified = exact_error_bounds(n_certified)
    assert lower_at_previous >= tol and upper_at_certified <= tol
    assert n_certified == 500

    # The conventional bound E_N < 1/(N+1) suffices at N=999.
    n_standard = next(n for n in range(1, 1001) if Fraction(1, n + 1) <= tol)
    assert n_standard == 999

    # PYTHON: Each entry in cumsum is the sum of exactly N terms.
    # log(2) is only a numerical reference, not used to certify the stopping rule.
    n = np.arange(1, 1101)
    sign = np.where(n % 2 == 1, 1, -1)
    sums = np.cumsum(sign / n)
    error = np.abs(log(2) - sums)
    assert error[n_certified - 2] > float(tol) > error[n_certified - 1]
    print(f"First-omitted-term bound guarantees accuracy with N={n_standard}.")
    print(f"N=499: error > {float(lower_at_previous):.9f}, so 499 fails.")
    print(f"N=500: error < {float(upper_at_certified):.9f}, so 500 succeeds.")
    print("The error integral decreases with N. Therefore 500 terms is the exact minimum.")
    print(f"Floating-point estimate of the error at N=500: {error[499]:.9f}.")

    fig, (left, right) = figure(args, "10", "How many terms are enough?")
    left.loglog(n, error, color=TEAL, lw=2, label=r"Observed $|\ln 2-S_N|$")
    left.loglog(n, 1 / (n+1), "--", color=BLUE, lw=1.7, label="First omitted term")
    left.axhline(float(tol), color=RUST, lw=1.2, ls=":", label="Error tolerance")
    for threshold, color in [(n_certified, TEAL), (n_standard, BLUE)]:
        left.scatter([threshold], [float(tol)], color=color, s=35, zorder=5)
    left.set(title="Convergence does not tell you when to stop", xlabel="Number of terms (log scale)",
             ylabel="Absolute error (log scale)")
    left.legend(loc="upper right")

    zoom = np.arange(495, 506)
    bounds = np.array([tuple(float(b) for b in exact_error_bounds(int(i))) for i in zoom])
    right.fill_between(zoom, 1e6*bounds[:, 0], 1e6*bounds[:, 1], color=BLUE, alpha=0.19,
                       label="Proven error interval")
    right.plot(zoom, 1e6 * error[zoom-1], "o-", color=TEAL, lw=1.4, ms=4,
               label="Observed error")
    right.axhline(1e6 * float(tol), color=RUST, lw=1.2, ls=":", label="Tolerance")
    right.axvline(499, color=MUTED, lw=0.9, ls=":")
    right.axvline(500, color=MUTED, lw=0.9, ls=":")
    right.annotate("499 fails", (499, 1e6*error[498]), xytext=(-22, 47),
                   ha="right", textcoords="offset points",
                   arrowprops={"arrowstyle": "->", "color": RUST}, color=RUST)
    right.annotate("500 succeeds", (500, 1e6*error[499]), xytext=(20, -51),
                   textcoords="offset points", arrowprops={"arrowstyle": "->", "color": TEAL},
                   color=TEAL)
    right.set(title="Exact bounds decide between 499 and 500", xlabel="Number of terms",
              ylabel=r"Absolute error ($\times\,10^{-6}$)", ylim=(986.5, 1016))
    right.set_xticks([495, 497, 499, 500, 502, 505])
    right.legend(loc="upper right")
    save(fig, args, "10_alternating_log_series")


if __name__ == "__main__":
    main()
