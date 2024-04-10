import os
import argparse
import sys
import numpy as np
import pandas as pd

lexicase_pop_size = {'Pop_50': 50 ,'Pop_100': 100 ,'Pop_500': 500 ,'Pop_1000': 1000 ,'Pop_5000': 5000}

def ExperimentDir(exp):
    if exp == 0:
        return 'Contradictory-100/'
    elif exp == 1:
        return 'Contradictory-150/'
    elif exp == 2:
        return 'Contradictory-200/'
    elif exp == 3:
        return 'Contradictory-300/'
    elif exp == 4:
        return 'Contradictory-500/'
    else:
        sys.exit('UTILS: INVALID EXPERIMENT DIR TO FIND')

def BestSatisfactoryCoverage(file_name):
    # create pandas data frame of entire csv
    df = pd.read_csv(file_name)
    return df['satisfactory_coverage'].max()

def CheckDir(dir,exp,dump):
    # check if data dir exists
    if not os.path.isdir(dir):
        sys.exit('DATA DIRECTORY DOES NOT EXIST')

    best_sati_cov = []
    pop_size_l = []

    # Iterating through both keys and values
    for pop_size, size in lexicase_pop_size.items():
        # experiment dir
        exp_dir = dir + pop_size + '/' + exp

        if not os.path.isdir(exp_dir):
            print('SKIPPING:', exp_dir)
            continue
        print('Looking at:',exp_dir)

        # go through all the seeds
        for seed_dir, _, _ in os.walk(exp_dir):
            # skip root dir
            if exp_dir == seed_dir:
                continue

            file_dir = seed_dir + '/data.csv'

            # record data
            best_sati_cov.append(BestSatisfactoryCoverage(file_dir))
            pop_size_l.append(size)

    if os.path.exists(dump+exp) is False:
        os.mkdir(dump+exp)
    df = pd.DataFrame({'coverage': pd.Series(best_sati_cov), 'pop_size': pd.Series(pop_size_l)})
    df.to_csv(path_or_buf=dump+exp+'best.csv', index=False)

def main():
    # read in arguements
    parser = argparse.ArgumentParser()
    # where to save the results/models
    parser.add_argument("-d", "--data_dir", default="./", type=str)
    parser.add_argument("-du", "--dump_dir", default="./", type=str)
    parser.add_argument("-e", "--experiment", default=0, type=int)

    args = parser.parse_args()
    print('data_dir:', args.data_dir)
    print('experiment:', ExperimentDir(args.experiment))
    print('dump_dir:', args.dump_dir)
    print()

    print('GETTING BEST PERFORMANCES!')
    CheckDir(args.data_dir, ExperimentDir(args.experiment), args.dump_dir)
    print('FINISHED GATHERING PERFORMANCES!')

if __name__ == '__main__':
    main()
