#####################################################################################################
#
# Testing the diagnostic functions
#
# python3
#####################################################################################################

import sys
sys.path.append('../')
import numpy as np
from diagnostic import Diagnostic

def main():
    # construct diagnostic object to pass to EA
    diagnostic = Diagnostic(0)
    print('diagnostic:', diagnostic)

    for _ in range(20):
        print()
        x = np.array([5,5,4,3,2,1])
        np.random.shuffle(x)
        print('x:',x)
        print('ordered_exploitation:', diagnostic.ordered_exploitation(x))
        print('contradictory_objectives:', diagnostic.contradictory_objectives(x))
        print('multipath_exploration:', diagnostic.multipath_exploration(x))

if __name__ == '__main__':
    main()