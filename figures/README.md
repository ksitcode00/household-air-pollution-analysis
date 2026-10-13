# Portfolio figures

These figures present reviewed aggregate log(C+1) regression outputs from the
6 October 2026 analysis snapshot. No participant-level data are used by the
figure builder. Updated portfolio visuals were produced on 13 October 2026.

| Figure | Purpose |
| --- | --- |
| `research-overview.png` | A single homepage summary of the four pollutants across both exposure windows. |
| `adjusted-associations.png` | All eight selected-model ratios with numerical HC3 95% confidence intervals. |
| `adjustment-sensitivity.png` | Selected and full-background models on the same 179 households. |
| `analysis-workflow.png` | Original cohort, analytic sample, modeling sequence, and separate exploratory extensions. |

## Definitions

- `ratio`, `lower`, and `upper` in the [aggregate CSV](../results/aggregate_stove_associations.csv) are exponentiated stove-group coefficients and their HC3 t-based 95% interval limits.
- IDES is compared with traditional cookstoves. A ratio below 1 indicates a lower adjusted conditional geometric mean of C+1.
- The original cohort has 105 IDES and 75 traditional-stove households. Every displayed regression uses 179 complete cases; the cohort diagram is not a claim that all 180 entered those models.
- Full-background models retain the four forced terms and all five background terms. See [methodology](../docs/methodology.md).
- Point estimates and interval geometry use unrounded inputs; labels round to three decimal places. Plot axes are linear in the ratio.
- These are observational associations, not causal effects or exact percentage reductions in unshifted concentration. HC3 does not account for village dependence or post-selection uncertainty; intervals are not multiplicity-adjusted.
- Earlier SVG figures remain in version history and the repository as legacy graphics. The current README uses only the PNG snapshot above.

## Reproduce

```bash
python3 -m pip install -r scripts/requirements-figures.txt
python3 scripts/build_portfolio_figures.py
python3 -m unittest discover -s tests -v
```

Run from the repository root. The builder uses Georgia and Arial on macOS, or
DejaVu fonts on Linux. The tests validate the aggregate input, nonblank images,
text boundaries, and overlapping labels. Raw data access is not required.
