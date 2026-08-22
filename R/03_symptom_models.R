# Fit selected binary symptom models with odds-ratio summaries.
fit_binary_association <- function(df, outcome, exposure, covariates = character()) {
  variables <- c(outcome, exposure, covariates)
  model_data <- stats::na.omit(df[, variables, drop = FALSE])
  stats::glm(stats::reformulate(c(exposure, covariates), response = outcome), data = model_data, family = stats::binomial())
}

odds_ratio_table <- function(model) {
  estimate <- stats::coef(model)
  interval <- suppressMessages(stats::confint(model))
  data.frame(term = names(estimate), odds_ratio = exp(estimate), conf_low = exp(interval[, 1]), conf_high = exp(interval[, 2]), row.names = NULL)
}
