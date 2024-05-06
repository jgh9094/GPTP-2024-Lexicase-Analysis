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
                                  size = 0.5, linetype = "solid")
)

data_dir <- 'Paper_Data/Contradictory-100/'

# get over time data
over_time <- read.csv(paste(data_dir, 'ot.csv', sep = "", collapse = NULL), header = TRUE, stringsAsFactors = FALSE)
over_time$pop_size <- factor(over_time$pop_size, levels = NAMES)

# activation gene  coverage
lines_ac = over_time %>%
  group_by(pop_size, eval) %>%
  dplyr::summarise(
    min = min(activation_coverage),
    mean = mean(activation_coverage),
    max = max(activation_coverage)
  )
lines_ac$pop_size <- factor(lines_ac$pop_size, levels = NAMES)

over_time_ac = ggplot(lines_ac, aes(x=eval, y=mean, group = pop_size, fill = pop_size, color = pop_size, shape = pop_size)) +
  geom_ribbon(aes(ymin = min, ymax = max), alpha = 0.1) +
  geom_line(size = 0.5) +
  geom_point(data = filter(lines_ac, eval %% 100000000 == 0 & eval != 0), size = 1.5, stroke = 2.0, alpha = 1.0) +
  scale_y_continuous(
    name="Coverage",
    limits=c(0, 100),
    breaks=seq(0,100, 25),
    labels=c("0", "25", "50", "75", "100")
  ) +
  scale_x_continuous(
    name="Evaluation",
    limits = c(0,1520000000)
    
  ) +
  scale_shape_manual(values=SHAPE)+
  scale_colour_manual(values = cb_palette) +
  scale_fill_manual(values = cb_palette) +
  p_theme +
  guides(
    shape=guide_legend(nrow=1, title.position = "left", title = 'Population Size'),
    color=guide_legend(nrow=1, title.position = "left", title = 'Population Size'),
    fill=guide_legend(nrow=1, title.position = "left", title = 'Population Size')
  )

# satisfactory trait coverage
lines_sc = over_time %>%
  group_by(pop_size, eval) %>%
  dplyr::summarise(
    min = min(satisfactory_coverage),
    mean = mean(satisfactory_coverage),
    max = max(satisfactory_coverage)
  )
lines_sc$pop_size <- factor(lines_sc$pop_size, levels = NAMES)

over_time_sc = ggplot(lines_sc, aes(x=eval, y=mean, group = pop_size, fill = pop_size, color = pop_size, shape = pop_size)) +
  geom_ribbon(aes(ymin = min, ymax = max), alpha = 0.1) +
  geom_line(size = 0.5) +
  geom_point(data = filter(lines_sc, eval %% 100000000 == 0 & eval != 0), size = 1.5, stroke = 2.0, alpha = 1.0) +
  scale_y_continuous(
    name="Coverage",
    limits=c(0, 100),
    breaks=seq(0,100, 25),
    labels=c("0", "25", "50", "75", "100")
  ) +
  scale_x_continuous(
    name="Evaluation",
    limits = c(0,1520000000)
  ) +
  scale_shape_manual(values=SHAPE)+
  scale_colour_manual(values = cb_palette) +
  scale_fill_manual(values = cb_palette) +
  p_theme +
  guides(
    shape=guide_legend(nrow=1, title.position = "left", title = 'Population Size'),
    color=guide_legend(nrow=1, title.position = "left", title = 'Population Size'),
    fill=guide_legend(nrow=1, title.position = "left", title = 'Population Size')
  )

# get best coverage data
best <- read.csv(paste(data_dir, 'best.csv', sep = "", collapse = NULL), header = TRUE, stringsAsFactors = FALSE)
best$pop_size <- factor(best$pop_size, levels = NAMES)

best_plot = ggplot(best, aes(x = pop_size, y = coverage, color = pop_size, fill = pop_size, shape = pop_size)) +
  geom_flat_violin(position = position_nudge(x = .1, y = 0), scale = 'width', alpha = 0.2, width = 1.5) +
  geom_boxplot(color = 'black', width = .07, outlier.shape = NA, alpha = 0.0, size = 1.0, position = position_nudge(x = .16, y = 0)) +
  geom_point(position = position_jitter(width = 0.02, height = 0.0001), size = 1.5, alpha = 1.0) +
  scale_y_continuous(
    name="Coverage",
    limits=c(0, 100),
    breaks=seq(0,100, 25),
    labels=c("0", "25", "50", "75", "100"),
  ) +
  scale_x_discrete(
    name="Population Size"
  )+
  scale_shape_manual(values=SHAPE)+
  scale_colour_manual(values = cb_palette, ) +
  scale_fill_manual(values = cb_palette) +
  ggtitle('  Best satisfactory coverage')+
  p_theme 

left_col = plot_grid(
  over_time_sc + ggtitle("Satifactory trait coverage over time") +
    theme(legend.position = "none", axis.text.y = element_text(angle = 90, hjust = 0.5), axis.text.x = element_blank(), 
          axis.title.x = element_blank(), axis.ticks.x = element_blank()),
  over_time_ac + ggtitle("Activation gene coverage over time") +
    theme(legend.position = "none", axis.text.y = element_text(angle = 90, hjust = 0.5)),
  nrow=2,
  rel_heights = c(1.4,1.5),
  labels = c('      a','      b'),
  label_size = TSIZE
)

legend <- cowplot::get_legend(
  over_time_ac +
    guides(
      shape=guide_legend(nrow=1, title='Population size'),
      color=guide_legend(nrow=1, title='Population size'),
      fill=guide_legend(nrow=1, title='Population size')
    ) +
    theme(
      legend.position = "top",
      legend.box="verticle",
      legend.justification="center"
    )
)

base = plot_grid(
  left_col,
  best_plot+
    theme(legend.position = "none", axis.text.y = element_text(angle = 90, hjust = 0.5)),
  ncol=2,
  rel_widths = c(1.4,1.0),
  labels = c('       ','      c'),
  label_size = TSIZE
)

fig = plot_grid(
  ggdraw() + draw_label("Results for base contradictory objectives", fontface='bold', size = 24) + p_theme,
  base,
  legend,
  nrow = 3,
  rel_heights = c(0.1,1.5,.08),
  labels = c('','  ','    '),
  label_size = TSIZE)

save_plot(
  filename ="contradictory-100.pdf",
  fig,
  base_width=13,
  base_height=7
)
