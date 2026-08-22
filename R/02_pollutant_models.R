# Estimate stove-type associations with log-transformed pollutant measures.
fit_pollutant_models <- function(df) {
  outcomes <- intersect(c("log_PM10_24hr", "log_PM2.5_24hr", "log_PM1_24hr", "log_CO_24hr", "log_PM10_c", "log_PM2.5_c", "log_PM1_c", "log_BC_c", "log_CO_c"), names(df))
  stats::setNames(lapply(outcomes, function(outcome) {
    stats::lm(stats::reformulate("Type", response = outcome), data = df)
  }), outcomes)
}

summarize_pollutant_models <- function(models) {
  do.call(rbind, lapply(names(models), function(outcome) {
    coefficients <- stats::coef(summary(models[[outcome]]))
    term <- grep("Type", rownames(coefficients))[1]
    data.frame(outcome = outcome, estimate = coefficients[term, "Estimate"], std_error = coefficients[term, "Std. Error"], p_value = coefficients[term, grep("Pr", colnames(coefficients), value = TRUE)], row.names = NULL)
  }))
}
