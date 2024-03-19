import os
import argparse
import sys
import numpy as np

lexicase_configs = {'POP_50':[] ,'POP_100':[] ,'POP_500':[] ,'POP_1000':[] ,'POP_5000':[]}

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

    exp_dir = dir + exp
    # Iterating through both keys and values
    for pop_size, tracker in lexicase_configs.items():
        if not os.path.isdir(exp_dir + pop_size):
            tracker.append('NOT CREATED')
            continue

        rep_dir = exp_dir + pop_size
        for seed_dir, _, _ in os.walk(rep_dir):
                # skip root dir
                if rep_dir == seed_dir:
                    continue

                print('seed_dir:',seed_dir)


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
