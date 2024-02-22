#####################################################################################################
#
# Testing altering the genotype of single org
#
# python3
#####################################################################################################

import sys
sys.path.append('../')
import numpy as np
from org import Org
import copy as cp

mutation_prob = 0.07

def mutate(genotype):
    count = 0
    for i in range(len(genotype)):
        if np.random.choice([True,False], p=[mutation_prob,1-mutation_prob]):
            mut = np.random.normal(0.0,1.0)
            print('before:', genotype[i])
            # negative gene mutation
            if genotype[i] + mut < 0.0:
                genotype[i] = abs(genotype[i] + mut)
            # over 100.0 mutation
            elif genotype[i] + mut > 100.0:
                genotype[i] = 100.0 - (genotype[i] + mut - 100.0)
            # in the middle
            else:
                genotype[i] += mut
            print(' after:', genotype[i])
            count += 1

    return genotype, count

def main():
    # create org of dim 10
    dim = 5
    pop = []
    for _ in range(3):
        org = Org(dim)
        #evaluation simulated
        org.SetGenotype(np.random.uniform(0.0,1.0,dim))
        org.SetPhenotype(np.array([1]*dim))
        org.SetSatisfactoryTraits(np.array([1]*dim))
        org.CountSatisfactoryTraits()
        org.AggregateScore()
        org.FindActivationGene()
        pop.append(org)

    print('starting pop:')
    for org in pop:
        print(org.GetGenotype())
    print()

    # mutate each org
    new_genotypes = []
    mutation_cnts = []
    for org in pop:
        genotype,count = mutate(cp.deepcopy(org.GetGenotype()))
        new_genotypes.append(genotype)
        mutation_cnts.append(count)

    print()
    print('new pop')
    new_pop = []
    for geno,cnts,org in zip(new_genotypes,mutation_cnts, pop):
        offspring = Org(dim)
        # mutations were applied
        if 0 < cnts:
            offspring.SetGenotype(geno)
        # clone
        else:
            offspring.Inherit(org)
        new_pop.append(offspring)
        del org

    pop = []
    pop = new_pop
    for org in pop:
        print(org.GetGenotype())

if __name__ == '__main__':
    main()