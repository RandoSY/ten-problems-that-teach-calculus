"""Shared command-line and figure styling. All calculus stays in each lesson."""
import argparse
from pathlib import Path


TEAL = "#00766c"
BLUE = "#335f9b"
RUST = "#a64623"
INK = "#1b2d3a"
MUTED = "#526672"
LIGHT = "#e1e9ec"
GOLD = "#dfab60"


def options(description):
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--show", action="store_true", help="also open a graph window")
    parser.add_argument(
        "--out", type=Path, default=Path(__file__).resolve().parent / "figures",
        help="directory for saved figures (default: figures beside the scripts)",
    )
    parser.add_argument(
        "--format", choices=("png", "pdf", "svg"), default="png",
        help="output format (default: png; pdf and svg are vector formats)",
    )
    return parser.parse_args()


def figure(args, number, title, panels=2):
    import matplotlib as mpl

    if not args.show:
        mpl.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 11,
        "mathtext.fontset": "stix", "axes.titlesize": 13,
        "axes.titleweight": "semibold", "axes.labelcolor": INK,
        "text.color": INK, "axes.spines.top": False,
        "axes.spines.right": False, "axes.edgecolor": "#92a4ad",
        "xtick.color": MUTED, "ytick.color": MUTED,
        "grid.color": LIGHT, "grid.linewidth": 0.7,
        "legend.frameon": False, "legend.fontsize": 9.4,
        "savefig.facecolor": "white", "pdf.fonttype": 42, "svg.fonttype": "path",
    })
    fig, axes = plt.subplots(
        1, panels, figsize=(12, 5.05), layout="constrained",
    )
    fig.get_layout_engine().set(w_pad=0.17, h_pad=0.11, wspace=0.08)
    fig.suptitle(f"{number}   /   {title}", fontsize=20, fontweight="bold")
    for ax in (axes.flat if panels > 1 else [axes]):
        ax.set_axisbelow(True)
        ax.grid(True, axis="y")
    return fig, axes


def save(fig, args, stem):
    import matplotlib.pyplot as plt

    args.out.mkdir(parents=True, exist_ok=True)
    target = args.out / f"{stem}.{args.format}"
    fig.savefig(target, dpi=160)
    print(f"Figure saved: {target}")
    if args.show:
        plt.show()
    plt.close(fig)
