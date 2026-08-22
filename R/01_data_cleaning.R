# Load and prepare the restricted household air-pollution study data.
source("R/00_packages.R")
load_project_packages()

load_study_data <- function(path = "data/private/indoor_air_quality_raw.xlsx") {
  if (!file.exists(path)) stop("Restricted input not found. See data/README.md.", call. = FALSE)
  readxl::read_excel(path)
}

prepare_analysis_data <- function(df) {
  focus_villages <- c("Mohuldiya", "Nelung", "Sankarpur", "Jharbelda")
  df |>
    dplyr::mutate(
      focus_group = factor(ifelse(Village %in% focus_villages, "Focus", "Regular"), levels = c("Regular", "Focus")),
      Education_Grouped = factor(dplyr::case_when(
        `Q1F Education` %in% c(0, 1) ~ "No Formal Education",
        `Q1F Education` %in% c(2, 3) ~ "Primary or Middle School",
        `Q1F Education` %in% c(4, 5, 6, 7) ~ "High School and Above",
        TRUE ~ NA_character_
      )),
      Income_Grouped = factor(dplyr::case_when(
        `Q1J avg fam income` == 1 ~ "Less than Rs 5000",
        `Q1J avg fam income` == 2 ~ "Rs 5000 – 10,000",
        `Q1J avg fam income` %in% c(3, 4) ~ "More than Rs 10,000",
        TRUE ~ NA_character_
      )),
      Roof_Category = factor(dplyr::case_when(
        `Q4L roof material` %in% c(1, 3, 4) ~ "Non-Cement",
        `Q4L roof material` == 2 ~ "Cement",
        TRUE ~ NA_character_
      )),
      Type = factor(Type, levels = c("Traditional", "Improved"))
    )
}

# Example local use: df <- prepare_analysis_data(load_study_data())
