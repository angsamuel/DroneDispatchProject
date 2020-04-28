from scenario import *
from utility_bot import *
import sys
import io

def run_test(print_trace = True):
    '''
    This function runs a sample of the simulation.
    Parameters:
        print_trace         - optional toggle for printing trace.
    Returns:
        tuple(request_list, listOfPickupsAndDropoffs)
            request_list                - list of requested package orders
            listOfPickupsAndDropoffs    - list of timestamps from the solver
    '''
    a = Scenario(10,10,10,10,3,1)
    if print_trace:
        a.PrintScenario()

    u = UtilityBot()
    # grab a copy after populating the job list but before solving and popping
    request_list = a.requestsList.copy()
    
    if not print_trace:
        # Captue stdout for presentation layer
        old_stdout = sys.stdout
        new_stdout = io.StringIO() 
        sys.stdout = new_stdout
    u.Solve(a)
    if not print_trace:
        # Reset standard out
        output = new_stdout.getvalue()
        sys.stdout = old_stdout

    listOfPickupsAndDropoffs = []
    for drone in a.GetDrones():
        listOfPickupsAndDropoffs.append(drone.packageInteractions)
    if print_trace:
        print("\nPACKAGE TIMESTAMPS\n")
        print(listOfPickupsAndDropoffs)
    return (request_list, listOfPickupsAndDropoffs)

#testDrone = a.GetDrones()[0]
#print(testDrone.GetPath(a.warehouseList[0].idCode, a.warehouseList[1].idCode))