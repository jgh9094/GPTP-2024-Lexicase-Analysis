#####################################################################################################
#
# Diagnostic class for transforming a genotype into a phenotype.
# Both real vectors of the same cardinality.
#
# python3
#####################################################################################################

import numpy as np
import numpy.typing as npt
import copy as cp
from typeguard import typechecked
import sys

@typechecked # used for debugging purposes
class Diagnostic:
    # set the diagnsotic being used from the start
    def __init__(self, diagnostic: int):
        # make an actual diagnostic is being called
        if 0 <= diagnostic <= 3:
            self.diagnostic = diagnostic
        else:
            sys.exit('UNKNOWN DIAGNOSTIC IN DIAGNOSTIC CLASS CONSTRUCTOR')

    # takes in a genotype and applies appropriate genotype transformation
    def transform(self, genotype: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        if self.diagnostic == 0:
            return np.array(self.exploitation_rate(genotype))
        elif self.diagnostic == 1:
            return np.array(self.ordered_exploitation(genotype))
        elif self.diagnostic == 2:
            return np.array(self.contradictory_objectives(genotype))
        elif self.diagnostic == 3:
            return np.array(self.multipath_exploration(genotype))

    def exploitation_rate(self, genotype: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        phenotype = cp.deepcopy(genotype)
        return np.array(phenotype)

    def ordered_exploitation(self, genotype: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        phenotype = cp.deepcopy(genotype)
        index = len(genotype)

        # check when non-decreasing order is broken
        for i in range(len(genotype)-1):
            if genotype[i] < genotype[i+1]:
                index = i+1
                break

        # fill in zeros where non-decreasing order is broken
        for i in range(index, len(genotype)):
            phenotype[i] = 0.0

        return np.array(phenotype)

    def contradictory_objectives(self, genotype: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        # find max value and set it in phenotype
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

        # find right side zeros from max value, if any
        for i in range(lower, len(genotype)-1):
            if genotype[i] < genotype[i+1]:
                upper = i+1
                break
        # fill in right side zeros, if any
        for i in range(upper, len(genotype)):
            phenotype[i] = 0.0

        return np.array(phenotype)