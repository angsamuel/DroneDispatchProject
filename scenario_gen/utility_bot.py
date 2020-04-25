from scenario import * 

class UtilityBot():
    def CalculateUtility(self, distance, scenario):
        return 0
    def Solve(self, scenario):
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
                self.AdvanceTime()

            while len(readyOrders) > 0:
                #attempt to service order
                nextOrder = readyOrders[0]
                allDrones = scenario.GetDrones()
                possibleDrones = []
                for drone in allDrones:
                    #if drone is not full, we can use it
                    if drone.packages < drone.packageCapacity:
                        possibleDrones.append(drone)
                
                if len(possibleDrones) > 0:
                    #choose a drone to select
                    possibleDrones[0].ScheduleDelivery(readyOrders[0][1],readyOrders[0][2])
                    readyOrders.pop(0)
                else:
                    self.AdvanceTime()

    def PrintResults(self, scenario):
        print("")
    def AdvanceTime(self):
        self.timeStep += 1

