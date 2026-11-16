# Project review and teaching rationale

## What this project is meant to do

The ten-problem constraint forced us to choose questions that change how a learner reasons. An exercise earns a place when its mathematical move transfers beyond its original setting. The materials use the same problem numbers across the conceptual guide, worked solutions, and Python examples so a learner can move from purpose to derivation to computation without learning three unrelated sequences.

### Why each problem made the cut

| No. | Mathematical move | Decision the learner practices |
| --- | --- | --- |
| 01 | Limits and bounding | Can I establish a limit without needing to track every oscillation? |
| 02 | Derivative from first principles | What does an instantaneous rate mean when my measurements cover intervals? |
| 03 | Related rates | Which changes are linked by the same physical constraint? |
| 04 | Optimization | Which candidates are possible, and how do I know the best one wins? |
| 05 | Taylor approximation | How accurate is a prediction made from local information? |
| 06 | Definite integral | Do signs cancel for this report, or does every contribution count toward the total? |
| 07 | Fundamental Theorem of Calculus | Can I find how fast a total changes by looking only at its moving boundary? |
| 08 | Improper integral | Does a fading rate fade fast enough for the total to stay finite? |
| 09 | Differential equation and fit | What can I predict from a rule about change, and what evidence could show it is wrong? |
| 10 | Series remainder | What error bound tells me I have done enough work? |

## What was checked

- **Four PDFs, 33 pages.** Opened them with two PDF readers, rendered every page, and checked navigation and page order. Verified that the pilot ZIP contains byte-identical copies of the two published pilot PDFs. The [checksum manifest](../PDF-SHA256.txt) identifies the current published versions.
- **Mathematics.** Independently checked the central results for all ten problems and key numerical results for both pilots. For example, the continuous cart model gives 2/3 m of displacement and 2 m of travel. The pilot's four-slice estimate gives 0.625 m of displacement and happens to give exactly 2 m of travel. Those are different calculations, not conflicting answers. The series' exact remainder bounds rule out 499 terms and certify 500.
- **Python and figures.** Ran the ten scripts from a clean repository checkout, regenerated the ten figures, and compared the outputs with the included examples. These scripts demonstrate and check the calculations. A sampled plot is not a proof, and agreement between two software implementations does not validate a physical model.
- **Illustrations.** Checked the active cover's vector coordinates against the equations. The gold line is tangent to the parabola at (2, 4). Updated the conceptual guide's derivative figure to draw the position curve, two secants, and tangent from the same position law rather than from hand-placed coordinates. Removed the superseded raster cover from the current tree so it is not mistaken for the corrected artwork.
- **Documentation.** Corrected the stand-alone Python setup path and checked the links between the README, PDFs, scripts, and classroom materials.

## What has not been established

The student and teacher materials have not been tested with a class. The example cooling record is synthetic, and its interpolated crossing is an estimate, not a directly measured event. A predicted time can pass against that estimate without the full observed time bracket being narrow enough to guarantee a pass. The live version keeps later readings separate from the fit so they can challenge the prediction.

The first pilot should collect an initial explanation, a team report, and an individual transfer response for each lesson. Look for learners who can explain net versus total activity on a new record, and who can name a later measurement that could contradict their cooling prediction. Revise where learners still need a prompt before expanding the student investigations to the remaining eight problems.
