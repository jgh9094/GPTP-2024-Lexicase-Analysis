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

def main():
    # create org of dim 10
    dim = 5
    org,off1,off2,off3 = Org(dim),Org(dim),Org(dim),Org(dim)
    org.SetGenotype(np.random.uniform(0.0,1.0,dim))
    print('original:', org.GetGenotype())

    g1 = cp.deepcopy(org.GetGenotype())
    g1[0] = 0.0
    g2 = cp.deepcopy(org.GetGenotype())
    g2[-1] = 0.0

    off1.SetGenotype(g1)
    print('off1:', off1.GetGenotype())

    off2.SetGenotype(g2)
    print('off2:', off2.GetGenotype())
    print('original after:', org.GetGenotype())

    g = np.random.uniform(0.0,1.0,dim)
    print(type(g))
    print(type(g[0]))



if __name__ == '__main__':
    main()