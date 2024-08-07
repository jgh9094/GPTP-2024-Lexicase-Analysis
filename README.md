# Lexicase Selection Parameter Analysis: Varying Population Size and Test Case Redundancy with Diagnostic Metrics

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.11199990.svg)](https://doi.org/10.5281/zenodo.11199990)
[![supplemental](https://img.shields.io/badge/go_to-supplementary_material-98111e)](https://jgh9094.github.io/GPTP-2024-Lexicase-Analysis/Bookdown/Pages/)
[![data](https://img.shields.io/badge/go_to-data-9807FF)](https://osf.io/g5u9p/)


## Authors

- [Jose Guadalupe Hernandez](https://jgh9094.github.io/)
- [Anil Kumar Saini](https://theaksaini.github.io/)
- [Jason H. Moore](https://jasonhmoore.org/)

## Abstract

> Lexicase selection is a successful parent selection method in genetic programming that has outperformed other methods across multiple benchmark suites.
Unlike other selection methods that require explicit parameters to function, such as tournament size in tournament selection, lexicase selection does not.
However, if evolutionary parameters like population size and number of generations affect the effectiveness of a selection method, then lexicase's performance may also be impacted by these `hidden' parameters.
Here, we study how these hidden parameters affect lexicase's ability to exploit gradients and maintain specialists using diagnostic metrics from an existing benchmark suite that measures a selection scheme's ability to exploit and explore handcrafted search spaces.
By varying the population size with a fixed evaluation budget, we show that smaller populations tend to have greater exploitation capabilities, whereas larger populations tend to maintain more specialists.
We also consider the effect redundant test cases have on specialist maintenance, and find that high redundancy may hinder the ability to optimize and maintain specialists, even for larger populations.
Ultimately, we highlight that the interaction between population size, evaluation budget, and test cases must be carefully considered for the characteristics of the problem being solved.

## Repository guide

- `Data-Tools/`: all scripts related to data checking, collecting, and visualizing
  - `Check/`: scripts for checking data
  - `Collect/`: scripts for collecting data
  - `Stats/`: scripts for statistics tests
  - `Visualize/`: scripts for making plots
- `Hpc/`: all scripts to run experiments on HPC
- `Source/`: contains all Python scripts to run experiments.