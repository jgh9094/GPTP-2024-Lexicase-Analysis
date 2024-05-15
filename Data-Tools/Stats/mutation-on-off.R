# clean start
rm(list = ls())
cat("\014")
setwd('/Users/hernandezj45/Desktop/Repositories/GPTP-2024-Lexicase-Analysis/')

# libraries we are using
library(ggplot2)
library(cowplot)
library(dplyr)
library(PupillometryR)
library(scales) # to access break formatting functions

# experiment variables

NAMES = c(50,100,500,1000,5000)
SHAPE <- c(25,21,22,23,24)
cb_palette <- c('#648FFF','#FE6100','#DC267F','#785EF0','#FFB000')
TSIZE <- 22

p_theme <- theme(
  plot.title = element_text( face = "bold", size = 22, hjust=0.5),
  panel.border = element_blank(),
  panel.grid.minor = element_blank(),
  legend.title=element_text(size=22),
  legend.text=element_text(size=23),
  axis.title = element_text(size=23),
  axis.text = element_text(size=19),
  legend.position="bottom",
  panel.background = element_rect(fill = "#f1f2f5",
                                  colour = "white",
                                  linewidth = 0.5, linetype = "solid")
)

# mutation data
m_data_dir <- 'Paper_Data/Coupon_Collector/Mutation/Contradictory-100/'
m_over_time <- read.csv(paste(m_data_dir, 'ot.csv', sep = "", collapse = NULL), header = TRUE, stringsAsFactors = FALSE)
m_over_time$pop_size <- factor(m_over_time$pop_size, levels = NAMES)
m_over_time$mutation <- 'Yes'

# no mutation data
n_data_dir <- 'Paper_Data/Coupon_Collector/No_Mutation/Contradictory-100/'
n_over_time <- read.csv(paste(n_data_dir, 'ot.csv', sep = "", collapse = NULL), header = TRUE, stringsAsFactors = FALSE)
n_over_time$pop_size <- factor(n_over_time$pop_size, levels = NAMES)
n_over_time$mutation <- 'No'

# combine all data
over_time <- rbind(m_over_time,n_over_time)
over_time$mutation <- factor(over_time$mutation, levels=c('No','Yes'))

###################################################################################################################
# over time plots
###################################################################################################################


# pop size 100

# summary

filter(over_time, pop_size == 100 & eval == 1.5 * 10^9) %>%
  group_by(mutation) %>%
  dplyr::summarise(
    count = n(),
    na_cnt = sum(is.na(activation_coverage)),
    min = min(activation_coverage, na.rm = TRUE),
    median = median(activation_coverage, na.rm = TRUE),
    mean = mean(activation_coverage, na.rm = TRUE),
    max = max(activation_coverage, na.rm = TRUE),
    IQR = IQR(activation_coverage, na.rm = TRUE)
  )

# wilcoxon test
final_100 <- filter(over_time, pop_size == 100 & eval == 1.5 * 10^9)
# Yes > No: p = 6.163e-16
wilcox.test(final_100$activation_coverage ~ final_100$mutation,
            paired = FALSE, conf.int = FALSE, alternative = 'l')

# pop size 500

# summary

filter(over_time, pop_size == 500 & eval == 1.5 * 10^9) %>%
  group_by(mutation) %>%
  dplyr::summarise(
    count = n(),
    na_cnt = sum(is.na(activation_coverage)),
    min = min(activation_coverage, na.rm = TRUE),
    median = median(activation_coverage, na.rm = TRUE),
    mean = mean(activation_coverage, na.rm = TRUE),
    max = max(activation_coverage, na.rm = TRUE),
    IQR = IQR(activation_coverage, na.rm = TRUE)
  )


# wilcoxon test
final_500 <- filter(over_time, pop_size == 500 & eval == 1.5 * 10^9)
# Yes > No: p < 2.2e-16
wilcox.test(final_500$activation_coverage ~ final_500$mutation,
            paired = FALSE, conf.int = FALSE, alternative = 't')

# pop size 1000

# summary

filter(over_time, pop_size == 1000 & eval == 1.5 * 10^9) %>%
  group_by(mutation) %>%
  dplyr::summarise(
    count = n(),
    na_cnt = sum(is.na(activation_coverage)),
    min = min(activation_coverage, na.rm = TRUE),
    median = median(activation_coverage, na.rm = TRUE),
    mean = mean(activation_coverage, na.rm = TRUE),
    max = max(activation_coverage, na.rm = TRUE),
    IQR = IQR(activation_coverage, na.rm = TRUE)
  )

# wilcoxon test
final_1000 <- filter(over_time, pop_size == 1000 & eval == 1.5 * 10^9)

wilcox.test(final_1000$activation_coverage ~ final_1000$mutation,
            paired = FALSE, conf.int = FALSE, alternative = 't')