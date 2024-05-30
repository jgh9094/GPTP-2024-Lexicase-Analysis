# Lexidate validation evaluation strategy

## Authors

- [Jose Guadalupe Hernandez](https://jgh9094.github.io/)
- [Anil Kumar Saini](https://theaksaini.github.io/)
- [Jason H. Moore](https://jasonhmoore.org/)

## Overview

Link to all supplementary material: [here](https://jgh9094.github.io/GPTP-2024-Lexicase-Analysis/Bookdown/Pages/).
All data is available on the Open Science Framework [here](https://osf.io/g5u9p/).
NOTE: Data is still being generated.

### Abstract

> Lexicase selection is a parent selection method in genetic programming that has been shown to outperform other methods across multiple benchmark tasks.
In contrast to other selection methods with required parameters, such as tournament selection, lexicase operates without explicit parameters.
However, if parameters like population size and the number of generations can affect any selection method, then lexicase's performance can also be affected by these 'hidden' parameters.
Here, we study the effects of these hidden parameters on lexicase's ability to exploit gradients and specialist maintenance using a set of diagnostic metrics.
By varying the population size with a fixed evaluation budget, we show that smaller populations tend to have greater exploitation capabilities, whereas larger populations tend to maintain more specialists.
We also consider the effect redundant test cases have on specialist maintenance, and find that high redundancy may hinder the ability to optimize and maintain specialists, even for larger populations.
Additionally, we find that mutation affects specialist maintenance for smaller population sizes but not larger ones.
Ultimately, we highlight that population size must be carefully considered for the characteristics of the problem being solved.

## Repository guide

- `Data-Tools/`: all scripts related to data checking, collecting, and visualizing
  - `Check/`: scripts for checking data
  - `Collect/`: scripts for collecting data
  - `Stats/`: scripts for statistics tests
  - `Visualize/`: scripts for making plots
- `Hpc/`: all scripts to run experiments on HPC
  - `Mutation-On-Off/`: hpc scripts for mutation on/off experiments
- `Source/`: contains all Python scripts to run experiments.