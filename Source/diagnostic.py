#####################################################################################################
#
# Diagnostic script that transforms a genotype into a phenotype
#
# python3
#####################################################################################################

import numpy as np
import numpy.typing as npt
import copy as cp
from typeguard import typechecked

@typechecked
class Diagnostic:
    def __init__(self, diagnostic: int):
        self.diagnostic = diagnostic

    def transform(self, genotype: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        if self.diagnostic == 0:
            return self.exploitation_rate(genotype)
        elif self.diagnostic == 1:
            return self.ordered_exploitation(genotype)
        elif self.diagnostic == 2:
            return self.contradictory_objectives(genotype)
        elif self.diagnostic == 3:
            return self.multipath_exploration(genotype)
        else:
            print('UNKNOWN DIAGNOSTIC CALLED')
            exit(-1)

    def exploitation_rate(self, genotype: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        return genotype

    def ordered_exploitation(self, genotype: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        phenotype = cp.deepcopy(genotype)
        index = len(genotype)

        for i in range(len(genotype)-1):
            if genotype[i] < genotype[i+1]:
                index = i+1
                break

        for i in range(index, len(genotype)):
            phenotype[i] = 0.0

        return np.array(phenotype)

    def contradictory_objectives(self, genotype: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        phenotype = [0.0] * len(genotype)
        indx = np.argmax(genotype)
        phenotype[indx] = genotype[indx]
        return np.array(phenotype)

    def multipath_exploration(self, genotype: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        phenotype = cp.deepcopy(genotype)
        lower = np.argmax(genotype)
        upper = len(genotype)

        # fill in left side zeros, if any
        for i in range(lower):
            phenotype[i] = 0.0
        # find right side zeros, if any
        for i in range(lower, len(genotype)-1):
            if genotype[i] < genotype[i+1]:
                upper = i+1
                break
        # fill in right side zeros, if any
        for i in range(upper, len(genotype)):
            phenotype[i] = 0.0

        return np.array(phenotype)