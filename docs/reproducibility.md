# Reproducibility

[`R/00_packages.R`](../R/00_packages.R) documents the public pipeline dependencies. A package lockfile is not fabricated: a trustworthy `renv.lock` can only be generated in an approved environment with the actual installed package versions.

After obtaining data authorization, initialize it locally:

```r
install.packages(c("renv", "readxl", "dplyr", "ggplot2", "MASS", "stringr"))
renv::init()
renv::snapshot()
```

Never add restricted source files, derived participant-level tables, or private model outputs to Git.
