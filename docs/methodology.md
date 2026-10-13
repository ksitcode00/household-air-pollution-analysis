# Methodology

## Study design

The analysis compares indoor air-quality measurements from 105 households using Integrated Domestic Energy System (IDES) cookstoves and 75 households using traditional biomass cookstoves in rural Odisha, India.

## Analytical workflow

1. Clean survey, monitoring, household, and health variables; recode structural and socioeconomic fields into interpretable analytical groups.
2. Inspect pollutant distributions and transform skewed concentration outcomes on the log scale.
3. Compare pollutant patterns across cookstove type and household characteristics using descriptive statistics and appropriate group-difference tests.
4. Fit linear models with `log(C+1)` pollutant outcomes; exponentiated stove coefficients compare conditional geometric means of C+1, not exact percentage reductions in unshifted concentration C.
5. Evaluate respiratory and lung-function outcomes using logistic regression.
6. Conduct mediation, propensity-score/IPW, balance, and E-value sensitivity analyses to assess robustness of observational associations.

## Interpretation boundary

This is an observational cross-sectional analysis. Estimates are reported as adjusted associations and sensitivity analyses; they should not be interpreted as definitive causal effects.

## Current portfolio figure snapshot

The current figures show PM10, PM2.5, PM1, and CO for separate 24-hour and cooking-period outcomes. All eight selected models and all eight full-background models use the same 179 complete-case households from the original cohort of 180. One household lacks a kitchen-window code; no imputation was performed.

Stove group, electricity, Focus/Regular program category, and binary indoor/outdoor kitchen location are forced into every selected model. Education, income, roof, window/eaves ventilation, and household size enter the initial candidate set together. Whole-term partial F tests remove the nonforced term with the highest p-value while it exceeds 0.20. This is an exploratory retention criterion, not a significance or confounder-identification threshold. Full-background models retain all nine terms without backward removal.

The aggregate snapshot uses HC3 standard errors and two-sided t-based 95% intervals with residual degrees of freedom. Model-matched checks include GVIF, residual plots, studentized Breusch-Pagan tests, supplementary Shapiro-Wilk tests, Cook's distance, leverage, and externally studentized residuals. Diagnostic flags did not automatically exclude observations.

The original R Markdown and reusable R helpers preserve the broader exploratory work, including respiratory outcomes, mediation, and IPW sensitivity. The new figure builder reads checked aggregate model outputs; it does not refit household models or claim that the simplified R helpers reproduce this snapshot.

HC3 does not address village-level dependence or post-selection uncertainty. Confidence intervals are not multiplicity-adjusted. Comparisons between exposure windows are descriptive, not formal interaction tests.
