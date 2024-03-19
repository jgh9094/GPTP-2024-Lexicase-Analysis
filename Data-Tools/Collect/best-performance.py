import os
import argparse
import sys
import numpy as np
import pandas as pd

replicates = 50
lexicase_pop_size = {'Pop_50': 50 ,'Pop_100': 100 ,'Pop_500': 500 ,'Pop_1000': 1000 ,'Pop_5000': 5000}


def BestPerformance(file_name):
    # create pandas data frame of entire csv
    df = pd.read_csv(file_name)
    return df['performance'].max()

def CheckDir(dir,exp):
    # check if data dir exists
    if not os.path.isdir(dir):
        sys.exit('DATA DIRECTORY DOES NOT EXIST')

    # Iterating through both keys and values
    for pop_size, tracker in lexicase_pop_size.items():
        # experiment dir
        exp_dir = dir + pop_size + '/' + exp

        print('Looking at:',exp_dir)
        if not os.path.isdir(exp_dir):
            print('SKIPPING: EXPERIMENT DIR NOT CREATED')
            continue

        # go through all the seeds
        for seed_dir, _, _ in os.walk(exp_dir):
            # skip root dir
            if exp_dir == seed_dir:
                continue

            file_dir = seed_dir + '/data.csv'

            # record best performance
            performance = BestPerformance(file_dir)
            print('performance:', performance)


def main():
    # read in arguements
    parser = argparse.ArgumentParser()
    # where to save the results/models
    parser.add_argument("-d", "--data_dir", default="./", type=str)

    args = parser.parse_args()
    print('data_dir:', args.data_dir)
    print()

    print('CHECKING RUNS NOW!')
    CheckDir(args.data_dir, 'Exploitation/')
    print('FINISHED CHECKING!')

if __name__ == '__main__':
    main()
