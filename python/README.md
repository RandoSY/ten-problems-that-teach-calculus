# Ten Problems That Teach Calculus
## Python companion to the worked-solutions PDF

These ten small programs follow the same order as the [worked-solutions PDF](../docs/ten-problems-that-teach-calculus.pdf). See **sample-output.txt** for what a successful run prints. Each lesson shows how a step on paper becomes an operation in Python, prints the result and a check, then makes a two-panel Matplotlib figure. The supplied graphs are in **figures/**, so you can look through them before installing anything.

The lesson scripts are ordinary Python files, not notebooks. All the calculus is in the numbered files. The shared **plot_support.py** only handles formatting, command-line options, and saving. No symbolic math package is required.

## Run a lesson

Extract the ZIP first. Open a terminal in the extracted **calculus-python** folder. Python 3.9 or newer is required. The two external packages are NumPy and Matplotlib.

On Windows, using PowerShell or Command Prompt:

    py -m pip install -r requirements.txt
    py 06_distance_vs_displacement.py --show

On macOS or Linux, using a virtual environment:

    python3 -m venv .venv
    . .venv/bin/activate
    python -m pip install -r requirements.txt
    python 06_distance_vs_displacement.py --show

Omit **--show** to just save the figure, which works even if your machine has no graphical desktop. The default output is a PNG in **figures/**. Use **--out my_plots** to write elsewhere and **--format pdf** or **--format svg** to get vector graphics. Use **--help** on any script to see its options.

To rerun all ten and overwrite their sample PNGs:

    python run_all.py

On Windows, substitute **py** for **python** if that is how you launch Python. If you want to leave the supplied figures alone, run **python run_all.py --out my_plots**.

## Paper to Python

| Lesson | The move on paper | How the program expresses it |
|---|---|---|
| **01 — Oscillating limits** | Find two sequences and then use the squeeze theorem. | Form the exact phases, invert them, evaluate their sine values, and plot the shrinking envelope. |
| **02 — Instantaneous velocity** | Simplify the difference quotient before taking its limit. | Evaluate the original quotient for positive and negative nonzero offsets. Compare each result to `6 + h`. |
| **03 — Sliding ladder** | Differentiate a constraint that links two moving quantities. | Evaluate `-(x/y) * foot_rate` and check it by recomputing the height at nearby times. |
| **04 — Open-top box** | Find critical points, reject impossible cuts, and check endpoints. | Compute both roots, filter to the physical interval, and compare volumes at the remaining candidates. |
| **05 — Taylor exponential** | Approximate with a quadratic and bound the omitted remainder. | Evaluate `1 + x + x**2/2`, calculate the bound, and compare with the library exponential. |
| **06 — Distance and displacement** | Add signed changes for displacement or magnitudes for distance. | Build midpoint contributions with an array, then compare `changes.sum()` with `np.abs(changes).sum()`. |
| **07 — Moving integral edge** | Multiply the height at the upper edge by the speed of that edge. | Evaluate `integrand(edge(x)) * 2*x` and compare with finite differences of numerical areas. |
| **08 — Improper integral** | Accumulate over finite windows first, then let the cutoff grow. | Evaluate the exact finite total and check it by summing flow over short time slices. |
| **09 — Cooling coffee** | Fit a differential equation with one reading, then predict a later crossing. | Use logarithms to fit the rate constant and solve for the target time. Compare the formula to an Euler time-step loop. |
| **10 — Alternating log series** | Use exact bounds to find the first term count that meets the tolerance. | Compute bounds with rational arithmetic, stop when the upper bound certifies success, and use the lower bound to rule out 499 terms. |

## What to look for as you read the code

1. Predict what changes first. In lesson 06, will the two totals have the same sign and magnitude?
2. Find the numbered script and look for `# PAPER:` and the code immediately below it. Then compare the calculation with the figure.
3. Read the numerical check. Sampling a graph is not proof of a limit or a maximum. The analytical argument supplies the guarantee. The computation checks the implementation, illustrates the behavior, or both.
4. Change one thing and predict the effect. Try `n_demo = 17` in lesson 06 to see thinner Riemann rectangles. In lesson 07, move the sample `x0` to another positive value close to 0.9 to change the added strip. In lesson 09, try a smaller Euler step and compare its maximum deviation. The checks and some graph ranges are chosen for the original PDF problems, so larger edits may need matching changes.

### Suggested first run

Lesson 06 is the clearest starting point because the distinction on paper becomes one very small difference in code. The same sampled velocities and time widths go into both computations. Keeping the signs yields **2/3 m of displacement**. Taking their magnitudes yields **2 m of distance** in the limit. The printed midpoint table shows these two answers emerging as the slices get narrower.
