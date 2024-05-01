#####################################################################################################
#
# Evolutionary algorithm class that evolves orgs in the following order: evaluate, select, reproduce.
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
import multiprocessing as mp
import pandas as pd
import sys

# probability of mutation occuring at the gene level
MUTATION_PROB=0.007

@typechecked # for debugging purposes
class EA:
    def __init__(self, seed: int, pop_size: int, diagnostic: int, cores: int, redundancy: bool, redundancy_prop: float):
        # arguments needed to run
        self.seed = seed
        self.pop_size = pop_size
        self.diagnostic = Diagnostic(diagnostic)
        self.dimensionality_initial = 100 # default for this work
        self.rng = np.random.default_rng(seed)
        self.pop = []
        self.cores = cores

        # data tracking
        self.SetDataTracking(diagnostic=diagnostic)

        # set up test cases
        self.test_cases = self.SetTestCases(redundancy, redundancy_prop)
        # true dimensionality of the diagnostic configuration
        self.dimensionality = len(self.test_cases)

        # multiprocessing method, if needed (cores > 1)
        mp.set_start_method('fork')

    # Run the EA
    # EA runs until a max_eval evaluations are met
    def Evolve(self, max_evals: int):
        # intialize 'evolutionary time' variables
        gen = 0
        # after one iteration we have done this many evaluations
        evaluations = self.pop_size * self.dimensionality

        # step 0
        self.InitializePopulation()

        # repeat for max_gen
        while evaluations <= max_evals:
            # Step 1
            self.Evaluate()
            # Step 3
            parents = self.Selection()
            # Step 2
            self.RecordData(gen, evaluations, parents)
            # Step 4
            self.Reproduction(parents)

            # print current stats we are keeping track of
            self.CurrentStats()

            # increment gens and evaluations
            gen += 1
            evaluations += self.pop_size * self.dimensionality


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
        # if we can run in parallel
        if 1 < self.cores:
            # create new spanw rngs
            # https://numpy.org/doc/stable/reference/random/parallel.html
            spawns = self.rng.spawn(self.pop_size)

            with Pool(processes=self.cores) as pool:
                # https://superfastpython.com/multiprocessing-pool-issue-tasks/#How_To_Choose_The_Method
                return pool.map(self.Lexicase, spawns)
        else:
            return [self.Lexicase(self.rng) for _ in range(self.pop_size)]

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

        # multiple candidates left after processing all test cases
        parent = rng_.choice(candidates)

        assert 0 <= parent < self.pop_size
        return int(parent)

    def SetTestCases(self, flag: bool, prop: float) -> npt.NDArray[np.int64]:
        base = np.arange(0,self.dimensionality_initial)
        # one test case per objective
        if not flag:
            print('# of test cases:', len(base))
            return base
        # sample extra test cases per objective given by prop * dimensionality
        else:
            extra = int(prop * self.dimensionality_initial)
            sample = self.rng.choice(base, size=extra, replace=True)
            print('# of test cases:', len(np.concatenate((base, sample))))
            return np.concatenate((base, sample))


    #####################
    # REPRODUCTION STUFF
    #####################

    # iterate through each genome and apply mutations
    def Reproduction(self, parents: List[int]) -> None:
        # go though each parent id and produce offspring
        offspring_set = []
        for pid in parents:
            offspring = Org(self.dimensionality_initial)
            off_geno, mut_cnt = self.Mutate(cp.deepcopy(self.pop[pid].GetGenotype()))

            # at least one mutation was applied
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
        return genotype, 0

    # create the initial population
    def InitializePopulation(self) -> None:
        for _ in range(self.pop_size):
            # initialize org and get random vector
            org = Org(self.dimensionality_initial)
            org.SetGenotype(self.rng.uniform(0.0,1.0,self.dimensionality_initial))
            self.pop.append(org)


    #####################
    # DATA TRACKING STUFF
    #####################

    # what data are we tracking per diagnostics
    def SetDataTracking(self, diagnostic: int) -> None:
        # exploitation
        if diagnostic == 0 or diagnostic == 1:
            self.data_tracking_dict = {'performance': self.Performance,'satisfactory_solution': self.SatisfactorySolution, 'satisfactory_count': self.SatisfactoryCount}
        # contradictory
        elif diagnostic == 2:
            self.data_tracking_dict = {'performance': self.Performance,'activation_coverage': self.ActivationGeneCoverage,
                                 'satisfactory_coverage': self.SatisfacotoryTraitCoverage, 'minimum_activation_count': self.MinimumActivationCount}
        # multipath exploration
        elif diagnostic == 3:
            self.data_tracking_dict = {'performance': self.Performance,'activation_coverage': self.ActivationGeneCoverage,
                                 'satisfactory_coverage': self.SatisfacotoryTraitCoverage,'satisfactory_solution': self.SatisfactorySolution}
        # unknown diagnostic
        else:
            sys.exit('EVOLVER CLASS: UNKNOWN DIAGNOSTIC IN SetDataTracking()')

        self.data_dict = {'Gen':[], 'Eval': []}
        for key in self.data_tracking_dict:
            self.data_dict.update({key: []})

    # record
    def RecordData(self, gen: int, eval: int, parents: List[int]) -> None:

        self.data_dict['Gen'].append(gen)
        self.data_dict['Eval'].append(eval)
        for key,val in self.data_tracking_dict.items():
            if key == 'minimum_activation_count':
                self.data_dict[key].append(val(parents))
            else:
                self.data_dict[key].append(val())

    # find best performance in pop
    def Performance(self) -> np.float64:
        cur_best = -1.0
        for org in self.pop:
            if cur_best <  org.GetAggregate():
                cur_best = org.GetAggregate()

        return cur_best

    # find if satisfactory solution has been found yet
    def SatisfactorySolution(self) -> int:
        for org in self.pop:
            if org.GetCount() == self.dimensionality_initial:
                return 1
        return 0

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
        for obj in range(self.dimensionality_initial):
            # check that the objective is satisfied
            for org in self.pop:
                if 0.0 < org.SatisfiedTraitCheck(obj):
                    count += 1
                    break
        return int(count)

    # find solution with largest set of satisfactory traits
    def SatisfactoryCount(self) -> int:
        count = 0
        # go through each objective
        for org in self.pop:
            if count < org.GetCount():
                count = org.GetCount()
        return int(count)

    def MinimumActivationCount(self, parents: List[int]) -> int:
        coverage = []
        counts = {}
        for parent in parents:
            org = self.pop[parent]
            coverage.append(org.GetActivationGene())

        # Iterate over the list
        for gene in coverage:
            # If the item is already in the dictionary, increment its count
            if gene in counts:
                counts[gene] += 1
            # If the item is not in the dictionary, add it with a count of 1
            else:
                counts[gene] = 1

        return int(min(counts.values()))

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

    # print out all the current data being tracked
    def CurrentStats(self) -> None:
        data = ""
        for key,value in self.data_dict.items():
            data += key + '=' + str(value[-1]) + ' | '
        print(data, flush=True)