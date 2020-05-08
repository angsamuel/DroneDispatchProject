from scenario import *
from utility_bot import *
from utility_bot_dumb import *
from Greedy import *
import sys
import io
import copy


s = Scenario(25,25,5,25,50,5)
b = copy.deepcopy(s)
#s.PrintScenario()

u = UtilityBot()
ud = UtilityBotDumb()

dropoffDict = dict()
for order in s.requestsList:
    print(order)
    dropoffDict[order[0]] = order[3]
    print("dict at " + str(order[0]) + " is " + str(dropoffDict[order[0]]) )

u.Solve(s)
for drone in s.GetDrones():
    print("++++++++++++++")
    print(drone.packageInteractions)
    print(drone.instructions)
    print("--------------")


print(" ")
print("RESULTS----------------")
print(" ")

for drone in s.GetDrones():
    for pi in drone.packageInteractions:
        if pi[0] == 'dropoff':
            print(pi[2] - dropoffDict[pi[1]])
    




