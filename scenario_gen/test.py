from scenario import *


a = Scenario(10,10,10,10,3,1)
a.PrintScenario()

testDrone = a.GetDrones()[0]
print(testDrone.GetPath(a.warehouseList[0].idCode, a.warehouseList[1].idCode))