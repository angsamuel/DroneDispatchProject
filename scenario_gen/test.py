from scenario import *
from utility_bot import *


a = Scenario(10,10,10,10,3,1)
#a.PrintScenario()

u = UtilityBot()
u.Solve(a)

#testDrone = a.GetDrones()[0]
#print(testDrone.GetPath(a.warehouseList[0].idCode, a.warehouseList[1].idCode))