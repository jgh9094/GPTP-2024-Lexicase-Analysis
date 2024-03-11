#####################################################################################################
#
# Org class for holding genotype a phenotype.
# Also calculates genotype/phenotype metrics for analysis.
#
# python3
#####################################################################################################

import numpy as np
import copy as cp
from typeguard import typechecked
import numpy.typing as npt

# percentage of target value needed to reach satisfactory trait
ACCURACY=.99
# target value for each trait/gene
TARGET=100.0
# threshold to be considered satisfactory trait
THRESHOLD=ACCURACY*TARGET

@typechecked # for debugging purposes
class Org:
    def __init__(self, m: int):
        # dimensionality of everything
        self.dimensionality = m
        # dummy genotype assumed not set
        self.genotype = np.full(m, -1.0)
        self.spawned = False
        # dummy phenotype assumed not set
        self.phenotype = np.full(m, -1.0)
        self.evaluated = False
        # dummy satisfactory trait vector assumed not set
        self.satisfactory_traits = np.full(m, -1)
        self.satisfied = False
        # count for number of satisfactory traits assumed not set
        self.count = -1
        self.counted = False
        # aggregated phenotype assumed not yet set
        self.aggregate = -1.0
        self.aggregated = False
        # activation gene
        self.activation_gene = m
        self.agene_set = False
        # am I a clone?
        self.clone = False

    #####################
    # DATA CALCULATIONS
    #####################

    def SatisfiedTraitCheck(self, obj: int) -> np.int64:
        assert 0 <= obj < self.dimensionality
        assert np.all(self.satisfactory_traits >= 0.0)
        return self.satisfactory_traits[obj]

    def AggregateScore(self) -> None:
        assert not self.aggregated
        assert np.all(self.phenotype >= 0.0)
        self.aggregate = np.sum(self.phenotype) / self.dimensionality
        self.aggregated = True

    def FindActivationGene(self) -> None:
        assert not self.agene_set
        assert np.all(self.phenotype >= 0.0)
        self.activation_gene = np.argmax(self.phenotype)
        self.agene_set = True

    def FindSatisfactoryTraits(self) -> None:
        assert not self.satisfied
        assert np.all(self.satisfactory_traits < 0.0)
        self.satisfied = True

        for i in range(self.dimensionality):
            if THRESHOLD <= self.phenotype[i]:
                self.satisfactory_traits[i] = 1.0
            else:
                self.satisfactory_traits[i] = 0.0

    def CountSatisfactoryTraits(self) -> None:
        assert not self.counted
        assert self.satisfied
        assert np.all(self.satisfactory_traits >= 0.0)
        self.count = np.sum(self.satisfactory_traits)
        self.counted = True


    #####################
    # GETTERS
    #####################

    def GetGenotype(self) -> npt.NDArray[np.float64]:
        assert np.all(self.genotype >= 0.0)
        assert np.all(len(self.genotype) == self.dimensionality)
        return self.genotype

    def GetPhenotype(self) -> npt.NDArray[np.float64]:
        assert self.evaluated
        assert np.all(self.phenotype >= 0.0)
        return self.phenotype

    def GetPhenotypeTrait(self, obj: np.int64) -> np.float64:
        assert 0 <= obj < self.dimensionality
        assert np.all(self.phenotype >= 0.0)
        return self.phenotype[obj]

    def GetSatisfactoryTraits(self) -> npt.NDArray[np.float64]:
        assert self.satisfied
        assert np.all(self.satisfactory_traits >= 0.0)
        return self.satisfactory_traits

    def GetAggregate(self) -> np.float64:
        assert self.aggregated
        assert np.all(self.phenotype >= 0.0)
        return self.aggregate

    def GetCount(self) -> np.int64:
        assert self.counted
        assert np.all(self.satisfactory_traits >= 0.0)
        return self.count

    def GetClone(self) -> bool:
        assert self.spawned
        return self.clone

    def GetActivationGene(self) -> np.int64:
        assert self.activation_gene != self.dimensionality
        return self.activation_gene


    #####################
    # SETTERS
    #####################

    def SetGenotype(self, g_: npt.NDArray[np.float64]) -> None:
        assert not self.spawned
        assert np.all(self.genotype < 0.0)
        self.spawned = True
        self.genotype = cp.deepcopy(g_)

    def SetPhenotype(self, p_: npt.NDArray[np.float64]) -> None:
        assert not self.evaluated
        assert np.all(self.phenotype < 0.0)
        assert len(self.phenotype) == self.dimensionality
        self.evaluated = True
        self.phenotype = cp.deepcopy(p_)

    def SetSatisfactoryTraits(self, satis_: npt.NDArray[np.float64]) -> None:
        assert not self.satisfied
        assert np.all(self.satisfactory_traits < 0.0)
        self.satisfied = True
        self.satisfactory_traits = cp.deepcopy(satis_)

    def SetCount(self, c_: np.int64) -> None:
        assert not self.counted
        assert self.dimensionality > 0
        self.counted = True
        self.count = cp.deepcopy(c_)

    def SetAggregate(self, a_: np.float64) -> None:
        assert not self.aggregated
        assert self.dimensionality > 0
        self.aggregated = True
        self.aggregate = cp.deepcopy(a_)

    def SetActivationGene(self, s_: np.int64) -> None:
        assert not self.agene_set
        assert self.dimensionality > 0
        self.agene_set = True
        self.activation_gene = cp.deepcopy(s_)


    #####################
    # HELPERS
    #####################

    def Inherit(self, other_org: 'Org') -> None:
        assert not self.clone

        self.SetGenotype(other_org.GetGenotype())
        self.SetPhenotype(other_org.GetPhenotype())
        self.SetSatisfactoryTraits(other_org.GetSatisfactoryTraits())
        self.SetCount(other_org.GetCount())
        self.SetAggregate(other_org.GetAggregate())
        self.SetActivationGene(other_org.GetActivationGene())
        self.CloneTrue()

    def CloneTrue(self) -> None:
        assert not self.clone
        self.clone = True

    def print_org(self) -> None:
        print("dimensionality:", self.dimensionality)
        print("genotype:", self.genotype)
        print("spawned:", self.spawned)
        print("phenotype:", self.phenotype)
        print("evaluated:", self.evaluated)
        print("satisfactory_traits:", self.satisfactory_traits)
        print("satisfied:", self.satisfied)
        print("count:", self.count)
        print("counted:", self.counted)
        print("aggregate:", self.aggregate)
        print("aggregated:", self.aggregated)
        print("activation_gene:", self.activation_gene)
        print("agene_set:", self.agene_set)
        print("clone:", self.clone)