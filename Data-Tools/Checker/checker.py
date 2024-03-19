import os
import argparse
import sys
import numpy as np

lexicase_configs = {'Pop_50':[] ,'Pop_100':[] ,'Pop_500':[] ,'Pop_1000':[] ,'Pop_5000':[]}
does_not_exist = {'Pop_50':[] ,'Pop_100':[] ,'Pop_500':[] ,'Pop_1000':[] ,'Pop_5000':[]}

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

    # Iterating through both keys and values
    for pop_size, tracker in lexicase_configs.items():
        # experiment dir
        exp_dir = dir + pop_size + '/' + exp

        print('In:',exp_dir)
        if not os.path.isdir(exp_dir):
            tracker.append('NOT CREATED')
            continue

        # go through all the seeds
        for seed_dir, _, _ in os.walk(exp_dir):
            # skip root dir
            if exp_dir == seed_dir:
                continue

            file_dir = seed_dir + '/data.csv'
            print('file_dir:', file_dir)
            print('seed:', seed_dir.split('/')[-1].split('-')[0])
            return

            # now check if the data file exists in full data director
            if not os.path.isfile(file_dir):
                seed = 0
                does_not_exist[pop_size].append(seed)
                continue

    for pop_size, tracker in lexicase_configs.items():
        print(pop_size,':',tracker)

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
