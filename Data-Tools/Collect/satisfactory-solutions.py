import os
import argparse
import sys
import numpy as np
import pandas as pd

not_found_eval = 2000000000
# lexicase_pop_size = {'Pop_50': 50 ,'Pop_100': 100 ,'Pop_500': 500 ,'Pop_1000': 1000 ,'Pop_5000': 5000}
lexicase_pop_size = {'Pop_500': 500 ,'Pop_1000': 1000 ,'Pop_5000': 5000}

def SatifactoryFoundAt(file_name):
    # create pandas data frame of entire csv
    df = pd.read_csv(file_name)
    df = df[df['satisfactory_solution'] == 1]

    print(df)
    print('eval:', df['Eval'][0])

    exit()

    return df['performance'].max()

def CheckDir(dir,exp,dump):
    # check if data dir exists
    if not os.path.isdir(dir):
        sys.exit('DATA DIRECTORY DOES NOT EXIST')

    eval_sati_sol_fnd = []
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
            eval_sati_sol_fnd.append(SatifactoryFoundAt(file_dir))
            pop_size_l.append(size)

    df = pd.DataFrame({'evaluation': pd.Series(eval_sati_sol_fnd), 'pop_size': pd.Series(pop_size_l)})
    df.to_csv(path_or_buf=dump+'ssf.csv', index=False)

def main():
    # read in arguements
    parser = argparse.ArgumentParser()
    # where to save the results/models
    parser.add_argument("-d", "--data_dir", default="./", type=str)
    parser.add_argument("-du", "--dump_dir", default="./", type=str)

    args = parser.parse_args()
    print('data_dir:', args.data_dir)
    print()

    print('GETTING BEST PERFORMANCES!')
    CheckDir(args.data_dir, 'Exploitation/', args.dump_dir)
    print('FINISHED GATHERING PERFORMANCES!')

if __name__ == '__main__':
    main()
