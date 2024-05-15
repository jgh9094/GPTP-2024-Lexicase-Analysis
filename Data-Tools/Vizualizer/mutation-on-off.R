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

###################################################################################################################
# over time plots
###################################################################################################################


# pop size 100

# activation gene  coverage
lines_ac = filter(over_time, pop_size == 100 & eval != 0) %>%
  group_by(mutation, eval) %>%
  dplyr::summarise(
    min = min(activation_coverage),
    mean = mean(activation_coverage),
    max = max(activation_coverage)
  )

# over time

ggplot(lines_ac, aes(x=eval, y=mean, group = mutation, fill = mutation, color = mutation, shape = mutation)) +
  geom_ribbon(aes(ymin = min, ymax = max), alpha = 0.1) +
  geom_line(size = 0.5) +
  geom_point(data = filter(lines_ac, eval %% 100000000 == 0 & eval != 0), size = 1.5, stroke = 2.0, alpha = 1.0) +
  scale_y_continuous(
    name="Coverage",
    limits=c(0, 40),
    breaks=seq(0,40, 10),
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
    shape=guide_legend(nrow=1, title.position = "left", title = 'Mutation'),
    color=guide_legend(nrow=1, title.position = "left", title = 'Mutation'),
    fill=guide_legend(nrow=1, title.position = "left", title = 'Mutation')
  )

# final population 
end_100 = filter(over_time, pop_size == 100 & eval == 1.5 * 10^9) %>%
  ggplot(., aes(x = mutation, y = activation_coverage, color = mutation, fill = mutation, shape = mutation)) +
  geom_flat_violin(position = position_nudge(x = .1, y = 0), scale = 'width', alpha = 0.2, width = 1.5) +
  geom_boxplot(color = 'black', width = .07, outlier.shape = NA, alpha = 0.0, size = 1.0, position = position_nudge(x = .16, y = 0)) +
  geom_point(position = position_jitter(width = 0.02, height = 0.0001), size = 1.5, alpha = 1.0) +
  scale_y_continuous(
    name="Coverage",
    # limits=c(0, 20),
    # breaks=seq(0,20, 5),¬
    # labels=c("0", "25", "50", "75", "100"),
  ) +
  scale_x_discrete(
    name="Mutation"
  )+
  scale_shape_manual(values=SHAPE)+
  scale_colour_manual(values = cb_palette, ) +
  scale_fill_manual(values = cb_palette) +
  ggtitle('Final activation gene coverage')+
  p_theme 



# pop size 500

# activation gene  coverage
lines_ac = filter(over_time, pop_size == 500 & eval != 0) %>%
  group_by(mutation, eval) %>%
  dplyr::summarise(
    min = min(activation_coverage),
    mean = mean(activation_coverage),
    max = max(activation_coverage)
  )

# over time

ggplot(lines_ac, aes(x=eval, y=mean, group = mutation, fill = mutation, color = mutation, shape = mutation)) +
  geom_ribbon(aes(ymin = min, ymax = max), alpha = 0.1) +
  geom_line(size = 0.5) +
  geom_point(data = filter(lines_ac, eval %% 100000000 == 0 & eval != 0), size = 1.5, stroke = 2.0, alpha = 1.0) +
  scale_y_continuous(
    name="Coverage",
    limits=c(30, 100),
    # breaks=seq(30,100, 10),
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
    shape=guide_legend(nrow=1, title.position = "left", title = 'Mutation'),
    color=guide_legend(nrow=1, title.position = "left", title = 'Mutation'),
    fill=guide_legend(nrow=1, title.position = "left", title = 'Mutation')
  )

# final population 
end_500 = filter(over_time, pop_size == 500 & eval == 1.5 * 10^9) %>%
  ggplot(., aes(x = mutation, y = activation_coverage, color = mutation, fill = mutation, shape = mutation)) +
  geom_flat_violin(position = position_nudge(x = .1, y = 0), scale = 'width', alpha = 0.2, width = 1.5) +
  geom_boxplot(color = 'black', width = .07, outlier.shape = NA, alpha = 0.0, size = 1.0, position = position_nudge(x = .16, y = 0)) +
  geom_point(position = position_jitter(width = 0.02, height = 0.0001), size = 1.5, alpha = 1.0) +
  scale_y_continuous(
    name="Coverage",
    # limits=c(0, 20),
    # breaks=seq(0,20, 5),
    # labels=c("0", "25", "50", "75", "100"),
  ) +
  scale_x_discrete(
    name="Mutation"
  )+
  scale_shape_manual(values=SHAPE)+
  scale_colour_manual(values = cb_palette, ) +
  scale_fill_manual(values = cb_palette) +
  ggtitle('Final activation gene coverage')+
  p_theme 


# pop size 1000

# activation gene  coverage
lines_ac = filter(over_time, pop_size == 1000 & eval != 0) %>%
  group_by(mutation, eval) %>%
  dplyr::summarise(
    min = min(activation_coverage),
    mean = mean(activation_coverage),
    max = max(activation_coverage)
  )

# over time

ggplot(lines_ac, aes(x=eval, y=mean, group = mutation, fill = mutation, color = mutation, shape = mutation)) +
  geom_ribbon(aes(ymin = min, ymax = max), alpha = 0.1) +
  geom_line(size = 0.5) +
  geom_point(data = filter(lines_ac, eval %% 100000000 == 0 & eval != 0), size = 1.5, stroke = 2.0, alpha = 1.0) +
  scale_y_continuous(
    name="Coverage",
    # limits=c(30, 100),
    # breaks=seq(30,100, 10),
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
    shape=guide_legend(nrow=1, title.position = "left", title = 'Mutation'),
    color=guide_legend(nrow=1, title.position = "left", title = 'Mutation'),
    fill=guide_legend(nrow=1, title.position = "left", title = 'Mutation')
  )

# final population 
end_1000 = filter(over_time, pop_size == 1000 & eval == 1.5 * 10^9) %>%
  ggplot(., aes(x = mutation, y = activation_coverage, color = mutation, fill = mutation, shape = mutation)) +
  geom_flat_violin(position = position_nudge(x = .1, y = 0), scale = 'width', alpha = 0.2, width = 1.5) +
  geom_boxplot(color = 'black', width = .07, outlier.shape = NA, alpha = 0.0, size = 1.0, position = position_nudge(x = .16, y = 0)) +
  geom_point(position = position_jitter(width = 0.02, height = 0.0001), size = 1.5, alpha = 1.0) +
  scale_y_continuous(
    name="Coverage",
    # limits=c(0, 20),
    # breaks=seq(0,20, 5),
    # labels=c("0", "25", "50", "75", "100"),
  ) +
  scale_x_discrete(
    name="Mutation"
  )+
  scale_shape_manual(values=SHAPE)+
  scale_colour_manual(values = cb_palette, ) +
  scale_fill_manual(values = cb_palette) +
  ggtitle('Final activation gene coverage')+
  p_theme 


# combine all together

legend <- cowplot::get_legend(
  end_100 +
    guides(
      shape=guide_legend(nrow=1, title='Mutation'),
      color=guide_legend(nrow=1, title='Mutation'),
      fill=guide_legend(nrow=1, title='Mutation')
    ) +
    theme(
      legend.position = "top",
      legend.box="verticle",
      legend.justification="center"
    )
)

center = plot_grid(
  end_100+
    ggtitle("Population size 100") +
    theme(legend.position = "none", axis.title.x=element_blank(), axis.text.y = element_text(angle = 90, hjust = 0.5),
          axis.ticks.x = element_blank(), axis.text.x = element_blank()),
  end_500+
    ggtitle("Population size 500") +
    theme(legend.position = "none",axis.title.y=element_blank(), axis.title.x=element_blank(), axis.text.y = element_text(angle = 90, hjust = 0.5),
          axis.ticks.x = element_blank(), axis.text.x = element_blank()),
  end_1000+
    ggtitle("Population size 1000") +
    theme(legend.position = "none",axis.title.y=element_blank(), axis.title.x=element_blank(), axis.text.y = element_text(angle = 90, hjust = 0.5),
          axis.ticks.x = element_blank(), axis.text.x = element_blank()),
  ncol=3,
  rel_widths = c(1.1,1.0,1.0),
  labels = c('     a','  b', '  c'),
  label_size = TSIZE
)

fig = plot_grid(
  ggdraw() + draw_label("Activation gene coverage in final population", fontface='bold', size = 24) + p_theme,
  center,
  legend,
  nrow = 3,
  rel_heights = c(0.17,1.5,.12),
  labels = c('','  ','    '),
  label_size = TSIZE)


save_plot(
  filename ="muation-exp.pdf",
  fig,
  base_width=13,
  base_height=5
)




