"""Optimize the volume of a box folded from a 12-by-20-inch sheet."""
import numpy as np
from matplotlib.patches import Rectangle

from plot_support import INK, MUTED, RUST, TEAL, figure, options, save


def volume(x, width, length):
    return x * (width - 2 * x) * (length - 2 * x)


def main():
    args = options(__doc__)
    width, length = 12.0, 20.0
    edge = min(width, length) / 2

    # PAPER: Expand V = W*L*x - 2*(W+L)*x^2 + 4*x^3, then differentiate.
    # PYTHON: Solve V'=12*x^2 - 4*(W+L)*x + W*L=0 with the quadratic formula.
    a, b, c = 12, -4 * (width + length), width * length
    discriminant = b**2 - 4 * a * c
    roots = sorted((-b + sign * np.sqrt(discriminant)) / (2 * a) for sign in (-1, 1))

    # PAPER: A continuous function attains a maximum on [0, edge]. Only
    # endpoints and admissible critical points can be that maximum.
    inside = [x for x in roots if 0 < x < edge]
    candidates = [0.0, *inside, edge]
    best = max(candidates, key=lambda x: volume(x, width, length))
    max_volume = volume(best, width, length)

    grid = np.linspace(0, edge, 1201)
    sampled_best = grid[np.argmax(volume(grid, width, length))]
    assert len(inside) == 1 and abs(best - sampled_best) <= edge / (len(grid) - 1)
    print(f"Physical cut domain: [0, {edge:g}] in.")
    print("Derivative roots:", ", ".join(f"{x:.5f} in" for x in roots))
    for x in candidates:
        print(f"Candidate x = {x:.5f} in -> V = {volume(x, width, length):.5f} cubic in")
    print(f"Maximum: cut {best:.5f} in, volume {max_volume:.5f} cubic in.")
    print(f"Dense sampling gives x = {sampled_best:.5f} in (a check, not a proof).")

    fig, (left, right) = figure(args, "04", "The largest open-top box")
    left.grid(False)
    left.add_patch(Rectangle((0, 0), length, width, facecolor="#e7f3f1", edgecolor=INK, lw=1.3))
    left.add_patch(Rectangle((best, best), length-2*best, width-2*best,
                             facecolor="#b6ddd7", edgecolor=TEAL, ls="--", lw=1.5))
    for xx in (0, length - best):
        for yy in (0, width - best):
            left.add_patch(Rectangle((xx, yy), best, best, facecolor="#f2d7c7",
                                     edgecolor=RUST, lw=1.0, hatch="//"))
    left.text(length / 2, width / 2, "Box base", ha="center", va="center", color=INK)
    left.annotate(f"Cut {best:.2f} in", (length-best/2, width-best/2),
                  xytext=(-8, 26), textcoords="offset points", ha="right",
                  arrowprops={"arrowstyle": "->", "color": RUST}, color=RUST)
    left.set(title="The cut determines all three dimensions", xlabel="Sheet length (in)",
             ylabel="Sheet width (in)", aspect="equal", xlim=(-0.6, length+0.6),
             ylim=(-0.6, width+2.6))

    right.plot(grid, volume(grid, width, length), color=TEAL, lw=2.3)
    right.scatter([0, edge], [0, 0], color=MUTED, s=45, zorder=4, label="Collapsed endpoints")
    right.scatter([best], [max_volume], color=RUST, s=55, zorder=4, label="Admissible maximum")
    right.axvline(best, color=MUTED, lw=1, ls=":")
    right.set(title="Only the physical domain is plotted", xlabel="Cut size (in)",
              ylabel=r"Box volume (in$^3$)", ylim=(-24, max_volume*1.25))
    right.legend(loc="upper right")
    save(fig, args, "04_open_top_box")


if __name__ == "__main__":
    main()
