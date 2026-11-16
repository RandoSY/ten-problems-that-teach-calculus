"""Run the ten programs in order and regenerate their figures."""
import argparse
from pathlib import Path
import subprocess
import sys


def main():
    base = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=base / "figures")
    parser.add_argument("--format", choices=("png", "pdf", "svg"), default="png")
    args = parser.parse_args()

    lessons = sorted(base.glob("[0-9][0-9]_*.py"))
    if len(lessons) != 10:
        raise RuntimeError(f"Expected ten lesson scripts, found {len(lessons)}.")
    for script in lessons:
        print(f"\n--- {script.name} ---", flush=True)
        subprocess.run(
            [sys.executable, str(script), "--out", str(args.out.resolve()),
             "--format", args.format],
            check=True,
        )
    print(f"\nAll ten lessons ran successfully. Figures: {args.out.resolve()}")


if __name__ == "__main__":
    main()
