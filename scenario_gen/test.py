from scenario import *
from utility_bot import *


a = Scenario(10,10,10,10,3,1)
a.PrintScenario()

u = UtilityBot()
u.Solve(a)
listOfPickupsAndDropoffs = []
for drone in a.GetDrones():
    listOfPickupsAndDropoffs.append(drone.packageInteractions)

print("\nPACKAGE TIMESTAMPS\n")
print(listOfPickupsAndDropoffs)


#testDrone = a.GetDrones()[0]
#print(testDrone.GetPath(a.warehouseList[0].idCode, a.warehouseList[1].idCode))