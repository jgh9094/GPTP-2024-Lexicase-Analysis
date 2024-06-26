import os
import argparse
import sys
import numpy as np
import pandas as pd

resolution = 1000000
lexicase_pop_size = {'Pop_50': 50 ,'Pop_100': 100 ,'Pop_500': 500 ,'Pop_1000': 1000 ,'Pop_5000': 5000}
lexicase_resolution = {'Pop_50': 50 ,'Pop_100': 100 ,'Pop_500': 500 ,'Pop_1000': 1000 ,'Pop_5000': 1}
performance_tracker = {'pop_size': [] ,'performance': [], 'eval': []}
contradictory_tracker = {'pop_size': [] ,'activation_coverage': [], 'satisfactory_coverage': [], 'eval': []}

def ExperimentDir(exp):
    if exp == 0:
        return 'Exploitation/'
    elif exp == 1:
        return 'Contradictory-100/'
    elif exp == 2:
        return 'Contradictory-150/'
    elif exp == 3:
        return 'Contradictory-200/'
    elif exp == 4:
        return 'Contradictory-300/'
    elif exp == 5:
        return 'Contradictory-500/'
    else:
        sys.exit('UTILS: INVALID EXPERIMENT DIR TO FIND')

def ExperimentAcro(exp):
    if exp == 0:
        return 'Exploitation/'
    elif exp == 1:
        return 'Contradictory-100/'
    elif exp == 2:
        return 'Contradictory-150/'
    elif exp == 3:
        return 'Contradictory-200/'
    elif exp == 4:
        return 'Contradictory-300/'
    elif exp == 5:
        return 'Contradictory-500/'
    else:
        sys.exit('UTILS: INVALID EXPERIMENT ACRO TO FIND')

def PerformanceOverTime(file_name, pop_size):
    # create pandas data frame of entire csv
    df = pd.read_csv(file_name)
    df = df[df['Eval'] % resolution == 0]

    # record performance over time
    performance_tracker['performance'].append(0) # add 0 for the start of a run
    performance_tracker['performance'] += df['performance'].tolist()

    # record evaluations over time
    performance_tracker['eval'].append(0) # add 0 for the start of a run
    performance_tracker['eval'] += df['Eval'].tolist()

    # record contradictory data pop_size
    performance_tracker['pop_size'] += [pop_size] * int(len(df['performance']) + 1)

    return

def ContradictoryOverTime(file_name, pop_size):
    # create pandas data frame of entire csv
    df = pd.read_csv(file_name)
    df = df[df['Eval'] % resolution == 0]

    # record activation coverage over time
    contradictory_tracker['activation_coverage'].append(0) # add 0 for the start of a run
    contradictory_tracker['activation_coverage'] += df['activation_coverage'].tolist()

    # record satisfactory coverage over time
    contradictory_tracker['satisfactory_coverage'].append(0) # add 0 for the start of a run
    contradictory_tracker['satisfactory_coverage'] += df['satisfactory_coverage'].tolist()

    # record evaluations over time
    contradictory_tracker['eval'].append(0) # add 0 for the start of a run
    contradictory_tracker['eval'] += df['Eval'].tolist()

    # record contradictory data pop_size
    contradictory_tracker['pop_size'] += [pop_size] * int(len(df['activation_coverage']) + 1)

    return

def CheckDir(dir,exp,dump):
    # check if data dir exists
    if not os.path.isdir(dir):
        sys.exit('DATA DIRECTORY DOES NOT EXIST')

    exp_acro = ExperimentAcro(exp)
    exp = ExperimentDir(exp)

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

            # record data for exploitation diagnostics
            if exp_acro == 'Exploitation/':
                PerformanceOverTime(file_dir, size)
            else:
                ContradictoryOverTime(file_dir, size)

    # save the data
    if os.path.exists(dump+exp_acro) is False:
        os.mkdir(dump+exp_acro)
    if exp_acro == 'Exploitation/':
        df = pd.DataFrame(performance_tracker)
        df.to_csv(path_or_buf=dump+exp_acro+'ot.csv', index=False)
    else:
        df = pd.DataFrame(contradictory_tracker)
        df.to_csv(path_or_buf=dump+exp_acro+'ot.csv', index=False)

def main():
    # read in arguements
    parser = argparse.ArgumentParser()
    # where to save the results/models
    parser.add_argument("-d", "--data_dir", default="./", type=str)
    parser.add_argument("-e", "--experiment", default=0, type=int)
    parser.add_argument("-du", "--dump_dir", default="./", type=str)

    args = parser.parse_args()
    print('data_dir:', args.data_dir)
    print('experiment:', ExperimentDir(args.experiment))
    print('dump_dir:', args.dump_dir)
    print()

    print('GETTING OVERTIME DATA!')
    CheckDir(args.data_dir, args.experiment, args.dump_dir)
    print('FINISHED GATHERING OVERTIME DATA!')

if __name__ == '__main__':
    main()
