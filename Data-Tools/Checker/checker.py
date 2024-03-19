import os
import argparse
import sys
import numpy as np
import pandas as pd

evaluations = 1500000000
lexicase_success = {'Pop_50':[] ,'Pop_100':[] ,'Pop_500':[] ,'Pop_1000':[] ,'Pop_5000':[]}
does_not_exist = {'Pop_50':[] ,'Pop_100':[] ,'Pop_500':[] ,'Pop_1000':[] ,'Pop_5000':[]}
evals_not_met = {'Pop_50':[] ,'Pop_100':[] ,'Pop_500':[] ,'Pop_1000':[] ,'Pop_5000':[]}

def SortTrackers():
    for pop_size in lexicase_success:
        lexicase_success[pop_size].sort()
    for pop_size in does_not_exist:
        does_not_exist[pop_size].sort()
    for pop_size in evals_not_met:
        evals_not_met[pop_size].sort()


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

def CheckEvaluations(file_name):
    # create pandas data frame of entire csv
    try:
        df = pd.read_csv(file_name)
    except pd.errors.EmptyDataError:
        df = pd.DataFrame()

    # return not met
    if(df.shape[0] == 0):
        return 0

    gens = df['Eval'].to_list()

    return gens[-1]

def CheckDir(dir,exp):
    # check if data dir exists
    if not os.path.isdir(dir):
        sys.exit('DATA DIRECTORY DOES NOT EXIST')

    # Iterating through both keys and values
    for pop_size, tracker in lexicase_success.items():
        # experiment dir
        exp_dir = dir + pop_size + '/' + exp

        print('Looking at:',exp_dir)
        if not os.path.isdir(exp_dir):
            tracker.append('EXPERIMENT DIR NOT CREATED')
            continue

        # go through all the seeds
        for seed_dir, _, _ in os.walk(exp_dir):
            # skip root dir
            if exp_dir == seed_dir:
                continue

            file_dir = seed_dir + '/data.csv'
            seed = int(seed_dir.split('/')[-1].split('-')[0])

            # check if the data file exists
            if not os.path.isfile(file_dir):
                does_not_exist[pop_size].append(seed)
                continue

            # check if evaluation count is met
            if CheckEvaluations(file_dir) != evaluations:
                evals_not_met[pop_size].append(seed)
                continue

            lexicase_success[pop_size].append(seed)

    SortTrackers()

    print()
    print('#### SUMMARY #####')
    print()
    for pop_size, tracker in lexicase_success.items():
        print(pop_size,':',len(tracker))
        print('success seeds:',tracker)
        print('does_not_exist:', len(does_not_exist[pop_size]))
        print('does_not_exist:', does_not_exist[pop_size])
        print('evals_not_met:', len(evals_not_met[pop_size]))
        print('evals_not_met:', evals_not_met[pop_size])
        print()
    print('######################################')

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
