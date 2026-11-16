"""Compare two vanishing rates with different accumulated totals."""
import numpy as np

from plot_support import BLUE, MUTED, RUST, TEAL, figure, options, save


def flow(t):
    return t * np.exp(-t)


def amount(T):
    # PAPER: Integration by parts gives [-(t+1)*exp(-t)] evaluated at 0 and T.
    return 1 - (T + 1) * np.exp(-T)


def slow_rate(t):
    return 1 / (1 + t)


def midpoint_amount(T, n):
    dt = T / n
    grid = (np.arange(n) + 0.5) * dt
    return dt * flow(grid).sum()


def main():
    args = options(__doc__)
    windows = (1, 5, 10, 20)
    print("Cutoff T (min)   Exact finite total (L)   Midpoint check (L)   Slow total (L)")
    for T in windows:
        computed = midpoint_amount(T, 20000)
        exact = amount(T)
        assert np.isclose(computed, exact, rtol=0, atol=1e-7)
        print(f"{T:>8g}          {exact:.9f}              {computed:.9f}           {np.log1p(T):.6f}")
    print("As T -> infinity: (T+1)*exp(-T) -> 0, so the total approaches 1 L.")
    print("The slow comparison rate also -> 0, but its total log(1+T) is unbounded.")

    fig, (left, right) = figure(args, "08", "A finite total over infinite time")
    t = np.linspace(0, 12, 350)
    left.plot(t, flow(t), color=TEAL, lw=2.3, label=r"$t e^{-t}$")
    left.plot(t, slow_rate(t), "--", color=BLUE, lw=2.3, label=r"$1/(1+t)$")
    left.set(title="Both flow rates approach zero", xlabel="Time (min)", ylabel="Flow rate (L/min)")
    left.legend(loc="upper right")

    cutoff = np.geomspace(0.1, 1e4, 600)
    right.semilogx(cutoff, amount(cutoff), color=TEAL, lw=2.3, label=r"$1-(T+1)e^{-T}$")
    right.semilogx(cutoff, np.log1p(cutoff), "--", color=BLUE, lw=2, label=r"$\ln(1+T)$")
    right.axhline(1, color=MUTED, ls=":", lw=1.1, label="1 L limit")
    right.scatter(windows, [amount(T) for T in windows], color=RUST, s=31, zorder=4)
    right.set(title="Only one accumulated total levels off",
              xlabel=r"Cutoff $T$ (min, logarithmic scale)", ylabel="Accumulated amount (L)")
    right.legend(loc="upper left")
    save(fig, args, "08_improper_integral")


if __name__ == "__main__":
    main()
