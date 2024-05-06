# clean start
rm(list = ls())
cat("\014")
setwd('~/Desktop/Repositories/GPTP-2024-Lexicase-Analysis/')

# libraries we are using
library(dplyr)

# important vars
NAMES = c(50,100,500,1000,5000)
data_dir <- 'Paper_Data/Contradictory-100/'

# get best coverage data 
best <- read.csv(paste(data_dir, 'best.csv', sep = "", collapse = NULL), header = TRUE, stringsAsFactors = FALSE)
best$pop_size <- factor(best$pop_size, levels = NAMES)

best %>%
  group_by(pop_size) %>%
  dplyr::summarise(
    count = n(),
    na_cnt = sum(is.na(coverage)),
    min = min(coverage, na.rm = TRUE),
    median = median(coverage, na.rm = TRUE),
    mean = mean(coverage, na.rm = TRUE),
    max = max(coverage, na.rm = TRUE),
    IQR = IQR(coverage, na.rm = TRUE)
  )

# Kruscal-Wallis test
# p-value < 2.2e-16
kruskal.test(coverage ~ pop_size, data = best)

# Pairwise wlcoxon test
pairwise.wilcox.test(x = best$coverage, g = best$pop_size, p.adjust.method = "bonferroni",
                     paired = FALSE, conf.int = FALSE, alternative = 'g')

# activation gene coverage data

ac_ot <- read.csv(paste(data_dir, 'ot.csv', sep = "", collapse = NULL), header = TRUE, stringsAsFactors = FALSE)
ac_ot$pop_size <- factor(ac_ot$pop_size, levels = NAMES)

filter(ac_ot, eval == 1.5 * 10^9) %>%
  group_by(pop_size) %>%
  dplyr::summarise(
    count = n(),
    na_cnt = sum(is.na(activation_coverage)),
    min = min(activation_coverage, na.rm = TRUE),
    median = median(activation_coverage, na.rm = TRUE),
    mean = mean(activation_coverage, na.rm = TRUE),
    max = max(activation_coverage, na.rm = TRUE),
    IQR = IQR(activation_coverage, na.rm = TRUE)
  )

