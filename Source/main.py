#####################################################################################################
#
# Main script that runs experiments with a given set of configurations
#
# Command Line Inputs:
#
#           n_jobs: number of threads to use for parallelization
#       diagnostic: diagnostic used: 0 -> exploitation | 2 -> contradictory objectives
#   dimensionality: number of objectives for diagnostic
#      generations: number of generations for the EA
#         pop_size: number of solutions in the population
#      seed_offset: seed offset
#       redundancy: percentage of redundancy of objectives (redundancy * dimensionality -> the number of redundant objectives to append)
#         savepath: where are we saving things to
#
# Output: data files in the specified save path
#
# python3
#####################################################################################################

import argparse
from evolver import EA
import time


def main():
    # read in arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--diagnostic",       default=0,      type=int,
                        help="0->exploitaiton rate; 1->ordered exploitation; 2->contradictory objectives; 3->multipath exploration")
    parser.add_argument("--generations",      default=100,    type=int)
    parser.add_argument("--pop_size",         default=30,     type=int)
    parser.add_argument("--redundancy",       default=0,      type=int, help="True (1) or False (0)")
    parser.add_argument("--redundancy_prop",  default=0.0,    type=float)
    parser.add_argument("--seed",             default=0,      type=int)
    parser.add_argument("--cores",            default=0,      type=int)
    parser.add_argument("--savepath",         default="./",   type=str)

    # Parse all the arguments
    args = parser.parse_args()

    # print them out to be sure
    print('diagnostic:',args.diagnostic)
    print('generations:',args.generations)
    print('pop_size:',args.pop_size)
    print('redundancy:',args.redundancy)
    print('redundancy_prop:',args.redundancy_prop)
    print('savepath:',args.savepath)
    print('seed:',args.seed)
    print('cores:',args.cores)

    # pass all needed args
    evolver = EA(args.seed, args.pop_size, args.diagnostic, args.cores, bool(args.redundancy), args.redundancy_prop)

    # let it rip
    start_time = time.time()
    evolver.Evolve(args.generations)
    end_time = time.time()
    print("Runtime:", end_time - start_time)

    # save stuff
    evolver.Save(args.savepath)


if __name__ == '__main__':
    main()
    print('DONE!')