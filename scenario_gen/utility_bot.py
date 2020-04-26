from scenario import * 

class UtilityBot():
    def CalculateUtility(self, distance, scenario):
        return 0
    def Solve(self, scenario):
        self.scenario = scenario
        self.timeStep = 0
        ordersList = scenario.requestsList
        #all the orders we need to complete
        while len(ordersList) > 1:
            readyOrders = []
            #remove all orders ready to complete from list
            for order in ordersList:
                if order[3] <= self.timeStep:
                    readyOrders.append(ordersList.pop(0))

            if len(readyOrders)<1:
                self.AdvanceTime(scenario)

            #while len(readyOrders) > 0:
            for nextOrder in readyOrders:
                #attempt to service order
                allDrones = scenario.GetDrones()
                possibleDrones = []
                for drone in allDrones:
                    #if drone is not full, we can use it
                    if self.DroneCanDeliver(drone, nextOrder[1]):
                        possibleDrones.append(drone)
                

                #print("WOW")
                if len(possibleDrones) > 0:
                    #choose a drone to select
                    droneEvaluationList = [] #gonna store this as (drone, score)
                    for pdrone in possibleDrones:
                        droneEvaluationList.append((pdrone,self.UtilityHit(pdrone,nextOrder[1],self.scenario)))
                    
                    bestDrone = droneEvaluationList[0][0]
                    minCost = droneEvaluationList[0][1]
                    print(minCost)
                    for pair in droneEvaluationList:
                        if pair[1] < minCost:
                            minDrone = pair[0]
                            minCost = pair[1]


                    bestDrone.ScheduleDelivery(readyOrders[0][0],readyOrders[0][1],readyOrders[0][2])
                    readyOrders.remove(nextOrder)
            self.AdvanceTime(scenario)

    def PrintResults(self, scenario):
        print("")

    def DroneCanDeliver(self, drone, packageLocationID):
        #if drone is empty return true
        if drone.packages == 0:
            return True
        
        #if the package location exists in drones instructions then return true
        if drone.ScheduledToVisitLocation(packageLocationID):
            return True
        return False



    def AdvanceTime(self, scenario):
        self.timeStep += 1
        for drone in scenario.GetDrones():
            drone.UpdateTime(self.timeStep)
    
    def UtilityHit(self,drone,pickupID,scenario):
        if drone.packages > 0:
            return 1000000
        totalDrones = len(scenario.GetDrones())
        dronesInLocation =  len(scenario.GetDronesInLocation(drone.locationCode))
        dronesInNeighborhood = len(scenario.GetDronesInNeighborhood(drone.locationCode))
        totalWarehouses = scenario.wareHouseNum
        warehousesInNeighborhood = len(scenario.GetWarehousesInNeighborhood(drone.locationCode))
        #print((warehousesInNeighborhood))
        #print(dronesInNeighborhood)
        #print(dronesInLocation)
        distance = 0
        #if drone.packages == 0:
        distance = drone.GetPath(drone.locationCode, pickupID)[1]
        #else:
            #distance = drone.PredictDeliveryDistance()
        utilityHit = distance + distance * ((totalDrones/dronesInLocation)+(totalDrones/(2*(1+dronesInNeighborhood)))+(totalWarehouses/(1+warehousesInNeighborhood)))
        return utilityHit

