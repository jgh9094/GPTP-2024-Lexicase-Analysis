#####################################################################################################
#
# Main script that runs experiments with a given set of configurations
#
# Command Line Inputs:
#
#       diagnostic: diagnostic used: 0 -> exploitation | 2 -> contradictory objectives
#         pop_size: number of solutions in the population
#       redundancy: True (1) or False (0)
#  redundancy_prop: percentage of redundancy of objectives (redundancy * dimensionality -> the number of redundant objectives to append)
#             seed: seed offset
#            cores: number of cores to use for parallelization
#         savepath: where are we saving things to
#
# Output: data files in the specified save path
#
# python3
#####################################################################################################

import argparse
from evolver import EA
import time
import os

def main():
    # read in arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--diagnostic",       default=0,      type=int,
                        help="0->exploitaiton rate; 1->ordered exploitation; 2->contradictory objectives; 3->multipath exploration")
    parser.add_argument("--pop_size",         default=30,     type=int)
    parser.add_argument("--redundancy",       default=0,      type=int, help="True (1) or False (0)")
    parser.add_argument("--redundancy_prop",  default=0.0,    type=float)
    parser.add_argument("--seed",             default=0,      type=int)
    parser.add_argument("--cores",            default=1,      type=int)
    parser.add_argument("--savepath",         default="./",   type=str)

    # Parse all the arguments and print
    args = parser.parse_args()
    print('diagnostic:',args.diagnostic)
    print('pop_size:',args.pop_size)
    print('redundancy:',args.redundancy)
    print('redundancy_prop:',args.redundancy_prop)
    print('savepath:',args.savepath)
    print('seed:',args.seed)
    print('cores:',args.cores)

    # Check if the directory doesn't exist already
    if os.path.exists(args.savepath):
        print('REPLICATE ALREADY DONE')
        return

    # total number of evaluations allowed for this work
    evaluations = 1500000000

    # pass all needed args
    evolver = EA(args.seed, args.pop_size, args.diagnostic, args.cores, bool(args.redundancy), args.redundancy_prop)

    # let it rip
    start_time = time.time()
    evolver.Evolve(evaluations)
    end_time = time.time()
    print("Runtime:", end_time - start_time)

    print('CREATING DIRECTORY')
    os.makedirs(args.savepath)
    print("SUCCESSFULLY CREATED:",args.savepath)

    # save stuff
    evolver.Save(args.savepath)

if __name__ == '__main__':
    main()