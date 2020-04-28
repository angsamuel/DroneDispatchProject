from scenario import *
from utility_bot import *
import sys
import io

s = Scenario(5,5,1,50,5,2)
u = UtilityBot()
u.Solve(s)

#self,warehouseNum,dropNum,droneNum,requestNum,droneRange,droneCapacity
#testDrone = a.GetDrones()[0]
#print(testDrone.GetPath(a.warehouseList[0].idCode, a.warehouseList[1].idCode))
