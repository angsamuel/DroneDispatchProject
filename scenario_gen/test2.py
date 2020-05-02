from scenario import *
from utility_bot import *
import sys
import io

s = Scenario(100,300,30,200,10,10)
#s = Scenario(5,5,5,5,5000,5)
u = UtilityBot()
u.Solve(s)

for drone in s.GetDrones():
    print(drone.instructions)
#self,warehouseNum,dropNum,droneNum,requestNum,droneRange,droneCapacity
#testDrone = a.GetDrones()[0]
#print(testDrone.GetPath(a.warehouseList[0].idCode, a.warehouseList[1].idCode))
