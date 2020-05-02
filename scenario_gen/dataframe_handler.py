from test import *
import Greedy

import pandas as pd
pd_ver = pd.__version__

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

def run_trials(sp1, sp2, sp3, sp4, sp5, sp6 , num_trials = 10):
    '''
    Runs trials.
    Returns pandas dataframe of wait time by trial number.
    '''
    utility_trials = {}
    #Run num_trials trials and store in dictionary
    for trial_num in range(num_trials):
        # Pass a fresh scenario to each trial with the same properties
        #Utility test
        (request_list, listOfPickupsAndDropoffs) = run_test(Scenario(sp1, sp2, sp3, sp4, sp5, sp6), print_trace=False)
        df_util = generate_dataframe(request_list, listOfPickupsAndDropoffs)
        utility_trials.update(evaluate_trial(df_util, trial_num))
        #Greedy test
        dist_dict, job_dict = Greedy.Greedy(Scenario(sp1, sp2, sp3, sp4, sp5, sp6), sp1, sp2, sp3, sp4, sp5, sp6)
        

    df_utility_trials = pd.DataFrame.from_dict(utility_trials, orient='index', columns=['Mean Wait Time'])
    df_utility_trials.index.name = 'Trial #'
    return df_utility_trials

def evaluate_batch(sp1, sp2, sp3, sp4, sp5, sp6 , num_trials=30):
    '''
    This function will run a batch of num_trials trials. It will print out the average wait times for each trial
    and the overall average wait time across all batches.
    Note:
        Pandas version 1.0.0 and later have a new to_markdown function. 
        I've included this check for automatic running in earlier packages.
    '''
    df_trials = run_trials(sp1, sp2, sp3, sp4, sp5, sp6 , num_trials)
    if pd_ver[0] != '1':
            print(df_trials)
    else:
        print(df_trials.to_markdown())
    print('\nTotal Average wait time across {0} trials : {1:.6}'.format( num_trials, df_trials['Mean Wait Time'].mean() ))  

#Scenario 1: Small Example
sp1, sp2, sp3, sp4, sp5, sp6 = (10, 30, 5, 50, 10, 3)
evaluate_batch(sp1, sp2, sp3, sp4, sp5, sp6)

#Scenario 2: Large Example
#sp1, sp2, sp3, sp4, sp5, sp6 = (100, 300, 30, 200, 10, 10)

#Scenario 3: Low Warehouse
#sp1, sp2, sp3, sp4, sp5, sp6 = (2,30,10,100,10,2)
