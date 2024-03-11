import os
import argparse
import sys

# how many successful reps did we find
success_dict = {'5000':0,'1000':0,'500':0,'100':0,'50':0}

def ExperimentDir(exp):
    if exp == 0:
        return 'Exploitation/'
    elif exp == 1:
        return 'Specialist_Maintenance/0/'
    elif exp == 2:
        return 'Specialist_Maintenance/10/'
    elif exp == 3:
        return 'Specialist_Maintenance/50/'
    elif exp == 4:
        return 'Specialist_Maintenance/100/'
    elif exp == 5:
        return 'Specialist_Maintenance/500/'
    else:
        sys.exit('UTILS: INVALID EXPERIMENT DIR TO FIND')

def Checker(dir):
    EMPTY_DIRECTORIES = []
    UNFINISHED_RUNS = []
    for subdir, dirs, files in os.walk(dir):
            # skip root dir
            if subdir == dir:
                continue

            # folder is empty
            if os.path.exists(subdir + failed_pkl) is False and os.path.exists(subdir + data_pkl) is False and \
                os.path.exists(subdir + evaluated_pkl) is False and os.path.exists(subdir + scores_pkl) is False and \
                os.path.exists(subdir + fitted_pkl) is False:
                continue

def main():
    # read in arguements
    parser = argparse.ArgumentParser()
    # where to save the results/models
    parser.add_argument("-d", "--data_dir", default="./", required=False, nargs='?')
    # number of total replicates for each experiment
    parser.add_argument("-r", "--num_reps", default=40, required=False, nargs='?')
    # seed we are starting from for each experiment
    parser.add_argument("-s", "--seed", default=0, required=False, nargs='?')
    # experiment we want to get data for
    parser.add_argument("-e", "--experiment", default=0, required=False, nargs='?')

    args = parser.parse_args()
    data_dir = args.data_dir
    num_reps = int(args.num_reps)
    seed = int(args.seed)
    exp_dir = ExperimentDir(exp=int(args.experiment))

    print('EXPERIMENT DIR:', data_dir + exp_dir)

    success = 0
    EMPTY_DIRECTORIES = []
    UNFINISHED_RUNS = []

    for task_pos, task in enumerate(task_id_lists):
        task_limit = False
        for rep in range(num_reps):
            dir = data_dir + exp_dir + str(rep + seed + (task_pos * num_reps)) + '-' + str(task) + '/'

            # last folder we made it to
            if os.path.isdir(dir) is False:
                NOT_YET_CREATED.append(dir)
                continue

            # check if data file exists
            data_pkl = dir + 'data.pkl'
            failed_pkl = dir + 'failed.pkl'
            evaluated_pkl = dir + 'evaluated_individuals.pkl'
            scores_pkl = dir + 'scores.pkl'
            fitted_pkl = dir + 'fitted_pipeline.pkl'

            # folder is empty
            if not any(os.scandir(dir)):
                EMPTY_DIRECTORIES.append(dir)
                print(dir,': EMPTY')
                continue

            # failed runs
            if os.path.exists(failed_pkl):
                print(dir,': FAILED.PKL')
                FAILED_FILES.append(dir)
                continue

            # check if data csv reached generation expectation and not empty
            df = pkl.load(open(data_pkl,'rb'))
            if df.empty:
                print(dir,': DATA.PKL EMPTY')
                UNFINISHED_RUNS.append(dir)
                continue

            if max(df['gen'].to_list()) != GENERATIONS:
                print(f"{dir}: {max(df['gen'].to_list())} GEN REACHED")
                UNFINISHED_RUNS.append(dir)
                continue


    print()
    print('-'*150)
    print()

    print('FAILED FILES:')
    for err in FAILED_FILES:
        print(err)
    print('\nUNFINISHED RUNS:')
    print()
    for err in UNFINISHED_RUNS:
        print(err)
    print('\nEMPTY DIRS:')
    print()
    for err in EMPTY_DIRECTORIES:
        print(err)
    print('\nNONEXISTENT DIRS:')
    print()
    for err in NOT_YET_CREATED:
        print(err)


if __name__ == '__main__':
    main()
    print('FINISHED CHECKING RUNS')