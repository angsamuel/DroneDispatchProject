from test import *

import pandas as pd
pd_ver = pd.__version__

from scenario import *
from utility_bot import *

def generate_dataframe(request_list, listOfPickupsAndDropoffs):
    '''
    This function pulls out the relevant data for out calculations and stores them in a pandas dataframe.
    Parameters: 
        request_list                - list of initial requests for packages by the customers
        listOfPickupsAndDropoffs    - list of pickup and dropoff times logged by the solver
    Returns:
        df                          - a pandas dataframe containing:
                                        * timestamp the package was ordered
                                        * timestamp the packages was delivered
                                        * wait time for the package from time ordered
    '''
    # Pull out only the data we're concerned with for analysis
    job_starts = [(x[0], x[3]) for x in request_list]
    job_completions = [(x[1],x[2]) for x in listOfPickupsAndDropoffs[0][1::2]]
    df = pd.DataFrame.from_dict({x[0][0]: (x[1][1],x[0][1]) for x in zip(job_completions,job_starts)}\
        , orient='index',     columns=['Arrival Time', 'Delivery Time'])
    df.index.name = 'Package ID'
    df['Wait Time'] = df['Delivery Time'] - df['Arrival Time']
    return df
    
def evaluate_trial(df, trial_num):
    '''
    This function evaluates a single trial by calculating metrics and returning
    them as data in a dictionary entry keyed by the trial number
    '''
    average_wait_time = df['Wait Time'].mean()
    return {trial_num : (average_wait_time)}

def run_trials(scenario, num_trials = 10):
    '''
    Runs trials.
    Returns pandas dataframe of wait time by trial number.
    '''
    trials = {}
    #Run num_trials trials and store in dictionary
    for trial_num in range(num_trials):
        (request_list, listOfPickupsAndDropoffs) = run_test(scenario, print_trace=False)
        df = generate_dataframe(request_list, listOfPickupsAndDropoffs)
        trials.update(evaluate_trial(df, trial_num))

    df_trials = pd.DataFrame.from_dict(trials, orient='index', columns=['Mean Wait Time'])
    df_trials.index.name = 'Trial #'
    return df_trials

def evaluate_batch(scenario, num_trials=10):
    '''
    This function will run a batch of num_trials trials. It will print out the average wait times for each trial
    and the overall average wait time across all batches.
    Note:
        Pandas version 1.0.0 and later have a new to_markdown function. 
        I've included this check for automatic running in earlier packages.
    '''
    df_trials = run_trials(scenario, num_trials)
    if pd_ver[0] != '1':
            print(df)
    else:
        print(df_trials.to_markdown())
    print('\nTotal Average wait time across {0} trials : {1:.6}'.format( num_trials, df_trials['Mean Wait Time'].mean() ))    