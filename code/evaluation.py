from scenario import *
from utility_bot import *
from utility_bot_dumb import *
from Greedy import *
import sys
import io
import copy
import Greedy


def calculate_greedy_average(job_dict):
    job_list = []
    for job in job_dict.keys():
        entered_queue, completed, droneId = job_dict[job]
        job_list.append(completed - entered_queue)
        return sum(job_list) / len(job_list)


#EDIT THESE VALUES--------------------------------------------------------------------------
warehouseNum = 10
dropNum = 10
droneNum = 10
requestNum = 50
droneRange = 10
droneCapacity = 5 

tests = 5







greedy_avgs = []
utility_avgs = []

for i in range(0,tests):
    s = Scenario(warehouseNum, dropNum, droneNum, requestNum, droneRange, droneCapacity)
    b = copy.deepcopy(s)
    #s.PrintScenario()

    u = UtilityBot()
    ud = UtilityBotDumb()

    orderDict = dict()
    for order in s.requestsList:
        #print(order)
        orderDict[order[0]] = order[3]
        #print("dict at " + str(order[0]) + " is " + str(orderDict[order[0]]) )

    u.Solve(s)


    dist_dict, job_dict = Greedy.Greedy(b, warehouseNum, dropNum, droneNum, requestNum, droneRange, droneCapacity)
    greedy_average = calculate_greedy_average(job_dict)




    smartSum = 0

    for drone in s.GetDrones():
        for pi in drone.packageInteractions:
            if pi[0] == 'dropoff':
                smartSum += (pi[2] - orderDict[pi[1]])

    avgWait = smartSum / requestNum
    print(" ")
    print("trial " + str(i))
    print("average wait for utility dispatcher: " + str(avgWait) )
    print("average wait for greedy dispatcher: " + str(greedy_average))
    

    greedy_avgs.append(greedy_average)
    utility_avgs.append(avgWait)

print("")
print("FINAL RESULT-------------------------------")
print("average utility wait time (total): " + str(sum(utility_avgs)/len(utility_avgs)))
print("average greedy wait time (total): " + str(sum(greedy_avgs)/len(greedy_avgs)))




