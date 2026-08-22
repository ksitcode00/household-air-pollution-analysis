# Generate figures only in an approved local environment.
plot_pollutant_by_stove <- function(df, pollutant = "log_PM2.5_24hr") {
  if (!pollutant %in% names(df)) stop("Requested pollutant is not available.", call. = FALSE)
  ggplot2::ggplot(df, ggplot2::aes(x = Type, y = .data[[pollutant]], fill = Type)) +
    ggplot2::geom_boxplot(alpha = 0.8, outlier.alpha = 0.35) +
    ggplot2::labs(title = "Indoor pollutant concentration by stove type", x = "Stove type", y = pollutant) +
    ggplot2::theme_minimal(base_size = 12) + ggplot2::theme(legend.position = "none")
}

save_private_figure <- function(plot, filename) {
  dir.create("results/private", recursive = TRUE, showWarnings = FALSE)
  ggplot2::ggsave(file.path("results/private", filename), plot = plot, width = 8, height = 5, dpi = 300)
}
