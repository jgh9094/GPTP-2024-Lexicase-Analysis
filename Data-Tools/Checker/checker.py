import os
import argparse
import sys
import numpy as np

GENERATIONS = 200

def ExperimentDir(exp):
    if exp == 0:
        return 'Exploitation/'
    elif exp == 1:
        return 'Contradictory-0/'
    elif exp == 2:
        return 'Contradictory-10/'
    elif exp == 3:
        return 'Contradictory-50/'
    elif exp == 4:
        return 'Contradictory-100/'
    elif exp == 5:
        return 'Contradictory-500/'
    else:
        sys.exit('UTILS: INVALID EXPERIMENT DIR TO FIND')

def CheckDir(dir,exp):
    # check if data dir exists
    if not os.path.isdir(dir):
        sys.exit('DATA DIRECTORY DOES NOT EXIST')
    # check that experiment directory exists
    if not os.path.isdir(dir + exp):
        sys.exit('DATA DIRECTORY DOES NOT EXIST')

    exp_dir = dir + exp
    for rep_dir, _, _ in os.walk(exp_dir):
            # skip root dir
            if rep_dir == exp_dir:
                continue

            print('rep_dir:',rep_dir)


def main():
    # read in arguements
    parser = argparse.ArgumentParser()
    # where to save the results/models
    parser.add_argument("-d", "--data_dir", default="./", type=str)
    # number of total replicates for each experiment
    parser.add_argument("-e", "--experiment", default=0, type=int)

    args = parser.parse_args()
    print('data_dir:', args.data_dir)
    exp_dir = ExperimentDir(exp=int(args.experiment))
    print('experiment:', exp_dir)
    print()

    print('CHECKING RUNS NOW!')
    CheckDir(args.data_dir, exp_dir)
    print('FINISHED CHECKING!')

if __name__ == '__main__':
    main()
