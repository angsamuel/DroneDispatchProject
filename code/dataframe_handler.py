from test_engine import run_test
import Greedy
from scenario import Scenario
import copy

import pandas as pd
pd_ver = pd.__version__

def generate_utility_dataframe(request_list, listOfPickupsAndDropoffs):
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
    
def calculate_greedy_average(job_dict):
    job_list = []
    for job in job_dict.keys():
        entered_queue, completed, droneId = job_dict[job]
        job_list.append(completed - entered_queue)
    return pd.Series(job_list).mean()
def evaluate_trial(df, trial_num):
    '''
    This function evaluates a single trial by calculating metrics and returning
    them as data in a dictionary entry keyed by the trial number
    '''
    average_wait_time = df['Wait Time'].mean()
    return {trial_num : (average_wait_time)}

def run_trials(sp1, sp2, sp3, sp4, sp5, sp6 , num_trials = 10,print_trace=False):
    '''
    Runs trials.
    Returns pandas dataframe of wait time by trial number.
    '''
    utility_trials = {}
    greedy_trials = {}
    #Run num_trials trials and store in dictionary
    for trial_num in range(num_trials):
        greedy_scen = Scenanrio(sp1, sp2, sp3, sp4, sp5, sp6)
        util_scen = copy.deepcopy(greedy_scen)
        # Pass a fresh scenario to each trial with the same properties
        #Utility test
        (request_list, listOfPickupsAndDropoffs) = run_test(util_scen, print_trace=print_trace)
        df_util = generate_utility_dataframe(request_list, listOfPickupsAndDropoffs)
        utility_trials.update(evaluate_trial(df_util, trial_num))
        #Greedy test
        dist_dict, job_dict = Greedy.Greedy(greedy_scen, sp1, sp2, sp3, sp4, sp5, sp6)
        greedy_average = calculate_greedy_average(job_dict)
        greedy_trials.update({trial_num: greedy_average})
    df_utility_trials = pd.DataFrame.from_dict(utility_trials, orient='index', columns=['Mean Wait Time'])
    df_utility_trials.index.name = 'Trial #'

    df_greedy_trials = pd.DataFrame.from_dict(greedy_trials, orient='index', columns=['Mean Wait Time'])
    df_greedy_trials.index.name = 'Trial #'
    return df_utility_trials, df_greedy_trials

def evaluate_batch(sp1, sp2, sp3, sp4, sp5, sp6 , print_trace=False, num_trials=30):
    '''
    This function will run a batch of num_trials trials. It will print out the average wait times for each trial
    and the overall average wait time across all batches.
    Note:
        Pandas version 1.0.0 and later have a new to_markdown function. 
        I've included this check for automatic running in earlier packages.
    '''
    df_utility_trials, df_greedy_trials = run_trials(sp1, sp2, sp3, sp4, sp5, sp6 , num_trials, print_trace=print_trace)
    print('Greedy Trials')
    print(df_greedy_trials.to_markdown())
    print('Utility Trials')
    print(df_utility_trials.to_markdown())
    print('\nTotal Average wait time across {0} trials :\nGreedy: {1:.6}\nUtility: {2:.6}'.format( num_trials, df_greedy_trials['Mean Wait Time'].mean(), df_utility_trials['Mean Wait Time'].mean() ))  

def evaluate_scenario_batch(scenario_list, label, print_trace=False):
    '''
    This function takes a list of tuples containing the parameters specifying
    settings for a scenario
    '''
    for scenario_params in scenario_list:
        sp1, sp2, sp3, sp4, sp5, sp6 = scenario_params
        print(label)
        evaluate_batch(sp1, sp2, sp3, sp4, sp5, sp6, print_trace=print_trace)

def auto_run():
    #number of nodes
    evaluate_scenario_batch([(5,5,5,50,10,5)
    ,(10,10,5,50,10,5)\
   # ,(20,20,5,50,10,5)
   # ,(40,40,5,50,10,5)
    ,(80,80,5,50,10,5)]
    , 'number of nodes', print_trace=True)

    
    #number of requests
    evaluate_scenario_batch([(30,30,5,5,10,5)
    ,(30,30,5,10,10,5)
    ,(30,30,5,20,10,5)
    ,(30,30,5,40,10,5)
    ,(30,30,5,80,10,5)]
    , 'number of requests')

    #drone capacity
    evaluate_scenario_batch([(30,30,5,100,10,5)
    ,(30,30,5,100,10,10)
    ,(30,30,5,100,10,20)
    ,(30,30,5,100,10,40)
    ,(30,30,5,100,10,80)]
    , 'drone capacity')

    #number of drones
    evaluate_scenario_batch([(40,40,5,50,10,5)
    ,(40,40,10,50,10,5)
    ,(40,40,20,50,10,5)
    ,(40,40,80,50,10,5)]
    , 'number of drones')

def demo():
    evaluate_scenario_batch([(5,5,5,50,10,5)], 'demo')

#auto_run()
demo()