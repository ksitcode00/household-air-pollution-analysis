# R pipeline

These small scripts expose reusable stages from the full R Markdown workflow for code review.

| Script | Purpose |
|---|---|
| `00_packages.R` | Validates required packages |
| `01_data_cleaning.R` | Loads approved local data and creates analysis variables |
| `02_pollutant_models.R` | Fits log-scale pollutant models by stove type |
| `03_symptom_models.R` | Fits binary-outcome models and returns odds ratios |
| `04_visualization.R` | Generates local-only figures in `results/private/` |

The complete analysis remains in [`analysis/air_pollution_analysis.Rmd`](../analysis/air_pollution_analysis.Rmd). Private inputs and participant-level outputs must remain local.
