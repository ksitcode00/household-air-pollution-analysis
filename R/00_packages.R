# Dependency manifest for the public analysis pipeline.
required_packages <- c("readxl", "dplyr", "ggplot2", "MASS", "stringr")

load_project_packages <- function(packages = required_packages) {
  missing <- packages[!vapply(packages, requireNamespace, logical(1), quietly = TRUE)]
  if (length(missing)) {
    stop("Install required packages: ", paste(missing, collapse = ", "), call. = FALSE)
  }
  invisible(lapply(packages, library, character.only = TRUE))
}
