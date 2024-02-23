#####################################################################################################
#
# Evolutionary algorithm script that handels main evolutionary steps: evaluate, select, reproduce
#
# python3
#####################################################################################################

import numpy as np
from org import Org
from diagnostic import Diagnostic
from typeguard import typechecked
from typing import List
import numpy.typing as npt
import copy as cp
from multiprocessing import Pool
import pandas as pd

MUTATION_PROB=0.007

@typechecked
class EA:
    def __init__(self, seed: int, pop_size: int, diagnostic: int, cores: int, redundancy: bool, redundancy_prop: float):
        # stuff we need for overall run
        self.seed = seed
        self.pop_size = pop_size
        self.diagnostic = Diagnostic(diagnostic)
        self.dimensionality = 100
        self.rng = np.random.default_rng(seed)
        self.pop = []
        self.cores = cores

        # data tracking stuff
        self.SetDataTracking(diagnostic=diagnostic)

        # set up test cases
        self.test_cases = self.SetTestCases(redundancy, redundancy_prop)

    # 3 step EA
    def Evolve(self, max_gen):
        # step 0
        self.InitializePopulation()
        # repeat for max_gen
        for gen in range(max_gen+1):
            # Step 1
            # print('Start')
            self.Evaluate()
            # print('Evaluate')
            # Step 2
            self.RecordData(gen)
            # print('Record Data')

            # self.PrintPop(p=self.pop)
            # print()

            # Step 3
            parents = self.Selection()
            # print('Selection')
            # print()
            # print('parents:',parents)
            # Step 4
            self.Reproduction(parents)
            # print('Reproduction')

            # print('Generation:',gen)
            self.CurrentStats()

    #####################
    # EVALUATION STUFF
    #####################

    # evaluate solutions and assign scores
    def Evaluate(self):
        # quick checks
        assert self.pop_size == len(self.pop)

        # loop through pop
        for i in range(self.pop_size):
            # if clone we can skip, already has data set
            if self.pop[i].GetClone():
                continue

            # calculate scores for new solution
            phenotype = self.diagnostic.transform(self.pop[i].GetGenotype())
            self.pop[i].SetPhenotype(phenotype)
            self.pop[i].FindSatisfactoryTraits()
            self.pop[i].CountSatisfactoryTraits()
            self.pop[i].AggregateScore()
            self.pop[i].FindActivationGene()

    #####################
    # SELECTION STUFF
    #####################

    # identify pop_size parents
    def Selection(self) -> List[int]:
        parents = []

        # create new spanw rngs
        # https://numpy.org/doc/stable/reference/random/parallel.html
        spawns = self.rng.spawn(self.pop_size)

        # create Pools
        with Pool(processes=self.cores) as pool:
            # https://superfastpython.com/multiprocessing-pool-issue-tasks/#How_To_Choose_The_Method
            parents = pool.map(self.Lexicase, spawns)

        # print('parents:', parents)

        return parents

    # standard lexicase
    def Lexicase(self, rng_: np.random.Generator) -> int:
        candidates = [x for x in range(self.pop_size)]
        # will depend on the proportion of redundancy if any
        test_cases = cp.deepcopy(self.test_cases)
        rng_.shuffle(test_cases)

        # go through each case
        for case in test_cases:
            obj_scores = []
            # go through the current set of candidates and get scores
            for candidate in candidates:
                obj_scores.append(self.pop[candidate].GetPhenotypeTrait(case))
            # make sure we getting the correct amount of scores
            assert len(obj_scores) == len(candidates)

            max_score = max(obj_scores)
            filter = []
            for score,candidate in zip(obj_scores,candidates):
                if score == max_score:
                    filter.append(candidate)
            candidates = filter

            if len(candidates) == 1:
                assert 0 <= candidates[0] < self.pop_size
                return int(candidates[0])

        parent = rng_.choice(candidates)

        assert 0 <= parent < self.pop_size
        return int(parent)

    def SetTestCases(self, flag: bool, prop: float) -> npt.NDArray[np.int64]:
        base = np.arange(0,self.dimensionality)
        # one test case per objective
        if not flag:
            return base
        # sample extra test cases per objective given by prop * dimensionality
        else:
            extra = int(prop * self.dimensionality) + self.dimensionality
            return self.rng.choice(base, size=extra, replace=True)


    #####################
    # REPRODUCTION STUFF
    #####################

    # iterate through each genome and apply mutations
    def Reproduction(self, parents: List[int]) -> None:
        # go though each parent id and produce offspring
        offspring_set = []
        for pid in parents:
            offspring = Org(self.dimensionality)
            off_geno, mut_cnt = self.Mutate(cp.deepcopy(self.pop[pid].GetGenotype()))

            if 0 < mut_cnt:
                offspring.SetGenotype(off_geno)
            else:
                offspring.Inherit(self.pop[pid])

            offspring_set.append(offspring)

        # clear out old pop
        for org in self.pop:
            del org
        self.pop = []

        # set the offspring as the new pop
        self.pop = offspring_set

    # mutate an single genotype
    def Mutate(self, genotype: npt.NDArray[np.float64]) -> tuple[npt.NDArray[np.float64], int]:
        count = 0
        for i in range(len(genotype)):
            # add mutation or not?
            if self.rng.choice([True,False], p=[MUTATION_PROB,1-MUTATION_PROB]):
                mut = self.rng.normal(0.0,1.0)
                # negative gene mutation
                if genotype[i] + mut < 0.0:
                    genotype[i] = abs(genotype[i] + mut)
                # over 100.0 mutation
                elif genotype[i] + mut > 100.0:
                    genotype[i] = 100.0 - (genotype[i] + mut - 100.0)
                # in the middle
                else:
                    genotype[i] += mut
                count += 1

        return genotype, count

    # create the initial population
    def InitializePopulation(self) -> None:
        for _ in range(self.pop_size):
            # initialize org and get random vector
            org = Org(self.dimensionality)
            org.SetGenotype(self.rng.uniform(0.0,1.0,self.dimensionality))
            self.pop.append(org)

    #####################
    # DATA TRACKING STUFF
    #####################

    # what data are we tracking per diagnostics
    def SetDataTracking(self, diagnostic: int) -> None:
        # exploitation
        if diagnostic == 0 or diagnostic == 1:
            self.data_tracking_dict = {'performance': self.Performance,'satisfactory_solution': self.SatisfactorySolution}
        # contradictory
        elif diagnostic == 2:
            self.data_tracking_dict = {'performance': self.Performance,'activation_coverage': self.ActivationGeneCoverage,
                                 'satisfactory_coverage': self.SatisfacotoryTraitCoverage}
        # multipath exploration
        elif diagnostic == 3:
            self.data_tracking_dict = {'performance': self.Performance,'activation_coverage': self.ActivationGeneCoverage,
                                 'satisfactory_coverage': self.SatisfacotoryTraitCoverage,'satisfactory_solution': self.SatisfactorySolution}
        # unknown diagnostic
        else:
            print('UNKNOWN DIAGNOSTIC')
            exit(-1)

        self.data_dict = {'Generation':[]}
        for key in self.data_tracking_dict:
            self.data_dict.update({key: []})

    # record
    def RecordData(self, gen: int) -> None:

        self.data_dict['Generation'].append(gen)
        for key,val in self.data_tracking_dict.items():
            self.data_dict[key].append(val())

    # find best performance in pop
    def Performance(self) -> np.float64:
        cur_best = -1.0
        for org in self.pop:
            if cur_best <  org.GetAggregate():
                cur_best = org.GetAggregate()

        return cur_best

    # find if satisfactory solution has been found yet
    def SatisfactorySolution(self) -> bool:
        for org in self.pop:
            if org.GetCount() == self.dimensionality:
                return True
        return False

    # calculate population-level activation gene coverage
    def ActivationGeneCoverage(self) -> int:
        coverage = set()
        for org in self.pop:
            coverage.add(org.GetActivationGene())
        return int(len(coverage))

    # calculate population-level satisfactory trait coverage
    def SatisfacotoryTraitCoverage(self) -> int:
        count = 0
        # go through each objective
        for obj in range(self.dimensionality):
            # check that the objective is satisfied
            for org in self.pop:
                if 0.0 < org.SatisfiedTraitCheck(obj):
                    count += 1
                    break
        return int(count)

    #####################
    # SAVING DATA HELPERS
    #####################

    def Save(self, dir: str):
        pd.DataFrame(self.data_dict).to_csv(dir + 'data.csv', index=False)

    #####################
    # PRINTING HELPERS
    #####################

    # print stuff out the pop (e.g. genotype/phenotype)
    def PrintPop(self, p: List[Org]) -> None:
        for indx,org in enumerate(p):
            print(indx, ':', org.GetGenotype())
            # print(indx, ':', org.GetPhenotype())

    # print out all the current data being tracked
    def CurrentStats(self) -> None:
        data = ""
        for key,value in self.data_dict.items():
            data += key + '=' + str(value[-1]) + ' | '
        print(data, flush=True)