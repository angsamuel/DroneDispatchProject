
import math
from scenario import * 
class Drone():
    def __init__(self, idCode, locationCode, packageCapacity, droneRange, scenario):
        self.idCode = idCode
        self.locationCode = locationCode
        self.packageCapacity = packageCapacity
        self.packages = 0
        self.droneRange = droneRange
        self.droneFuel = droneRange
        self.scenario = scenario
        self.instructions = [] #tuple of instruction, location, time complete
        self.packageInteractions = []
        self.baseTime = 0
        self.instructionIndex = 0
        self.deliveryIndex = 0
    
    def ScheduleDelivery(self,packageID, pickupName, destinationName, t):
        self.packages += 1
        pathToPickup = []
        lastTime = self.baseTime
        
            
        

        
        #pathfind to pickup
        if len(self.instructions) == 0: 
            pathToPickup = self.GetPath(self.locationCode, pickupName)[0]
            self.instructions.append(("begin", self.locationCode,self.baseTime))
        elif self.instructionIndex < len(self.instructions):
            pathToPickup = self.GetPath(self.instructions[-1][1],pickupName)[0]
            lastTime = self.instructions[-1][2]
        else:
            pathToPickup = self.GetPath(self.instructions[-1][1],pickupName)[0]
        
        timeTracker = lastTime
        
        #append pickup instructions
        for i in range(1,len(pathToPickup)):
            stop = pathToPickup[i]
            if (self.instructions[-1][1],stop) in self.scenario.edgeWeightLabels:
                #print(self.instructions[-1][1])
                timeTracker += self.scenario.edgeWeightLabels[(self.instructions[-1][1],stop)]
            self.instructions.append((("flyto", stop,timeTracker)))

        if timeTracker < t:
            timeTracker = t
        #append pickup 
        self.packageInteractions.append(("pickup", packageID, timeTracker))

        #pathfind to dropoff
        pathToDropoff = self.GetPath(self.instructions[-1][1],destinationName)[0]

        #append dropoff instructions
        for i in range(1,len(pathToDropoff)):
            stop = pathToDropoff[i]
            if (self.instructions[-1][1],stop) in self.scenario.edgeWeightLabels:
                timeTracker += self.scenario.edgeWeightLabels[(self.instructions[-1][1],stop)]
            self.instructions.append(("flyto", stop,timeTracker))
        
        #append dropoff 
        self.packageInteractions.append(("dropoff", packageID, timeTracker))

    #add a way to remove packages
    def UpdateTime(self, time):            
        if self.instructionIndex < len(self.instructions):
            for i in range(self.instructionIndex, len(self.instructions)-1):
                if time > self.instructions[i][2]:
                    self.instructionIndex += 1
                    self.locationCode = self.instructions[i][1]
        for i in range(self.deliveryIndex,len(self.packageInteractions)):
            if self.packageInteractions[i][2] < time and self.packageInteractions[i][0] == "dropoff":
                self.deliveryIndex = i+1
                self.packages -= 1

        self.baseTime = time
    
    def GetNextLocation(self):
        if len(self.instructions) == 0:
            return self.locationCode
        elif self.instructionIndex == len(self.instructions) - 1:
            return self.instructions[self.instructionIndex][1]
        else:
            return self.instructions[self.instructionIndex+1][1]

    def ScheduledToVisitLocation(self, locationID, t):
        if self.instructionIndex >= len(self.instructions):
            return False
        for i in range(self.instructionIndex,len(self.instructions)):
            if self.instructions[i][1] == locationID:
                if self.instructions[i][2] >= t:
                    print("======")
                    print(t)
                    print(self.instructions[i][2])
                    print("======")
                    return True
        return False


    def h(self,startNode,goalNode):
        if startNode == goalNode:
            return 0
        sx = self.scenario.positions[startNode][0]
        sy = self.scenario.positions[startNode][1]
        gx = self.scenario.positions[goalNode][0]
        gy = self.scenario.positions[goalNode][1]
        return math.sqrt((gx-sx)*(gx-sx) + (gy-sy)*(gy-sy))

    #takes a starting location, and ending location and returns the best path between them taking drone range into account
    #returns (path list, path cost)
    #I will later add some memoization to make this more efficient    
    def GetPath(self, startNodeName, goalNodeName):
        if ((startNodeName,goalNodeName)) in self.scenario.pathDict:
            #print("SAVED PATH")
            return self.scenario.pathDict[(startNodeName,goalNodeName)] 
        self.seenNodes = []
        self.queue = []
        self.pathCosts = []
        self.pathFuel = []
        self.savedDistances = dict()

        self.seenNodes.append(startNodeName)
        self.savedDistances[(startNodeName,startNodeName)] = 0
        self.scenario.pathDict[(startNodeName,goalNodeName)] = self.AStar([startNodeName],goalNodeName,0,self.droneFuel)
        return self.scenario.pathDict[(startNodeName,goalNodeName)] 

    
    def AStar(self, path, goalNodeName, cost, fuelLeft):
        neighbors = self.scenario.GetGraph().neighbors(path[-1])

        for i in range(0,len(self.queue)):
            if self.queue[i] == path:
                del(self.queue[i])
                del(self.pathCosts[i])

        if path[-1] == goalNodeName:
            return (path,cost)
        else:
            for n in neighbors:
                if n not in self.seenNodes:
                    #print(self.scenario.edgeWeightLabels[(path[-1],n)])
                    #print(fuelLeft)
                    #print(self.scenario.edgeWeightLabels[(path[-1],n)] > fuelLeft)
                    if self.scenario.edgeWeightLabels[(path[-1],n)] <= fuelLeft: #ensure we can reach neighbor
                        newFuel = fuelLeft
                        #print("WOWEE")
                        #print(n)
                        if 'W' in n:
                            newFuel = self.droneRange
                        else:
                            newFuel -= self.scenario.edgeWeightLabels[(path[-1],n)]
                        self.seenNodes.append(n)
                        npath = path.copy()
                        npath.append(n)
                        self.queue.append(npath)
                        self.pathFuel.append(newFuel)
                        #append the new cost to the pathcosts
                        if (path[-1],n) in self.scenario.edgeWeightLabels:
                            self.pathCosts.append(float(self.scenario.edgeWeightLabels[path[-1],n]) + cost)
                            if (path[0],n) not in self.savedDistances:
                                self.savedDistances[(path[0],n)] = self.pathCosts[-1]
                        else:
                            self.pathCosts.append(float(self.edgeWeightLabels[n,path[-1]]) + cost)
                            if (path[0],n) not in self.savedDistances:
                                self.savedDistances[(path[0],n)] = self.pathCosts[-1]
        #print(queue)
        if len(self.queue) < 1:
            return ([],1000000)
        
        #choose next node to explore
        minValue = 1000000
        minDex = -1
        for i in range(0,len(self.queue)):
            value = self.pathCosts[i] #g cost
            value += self.h(path[-1],goalNodeName)
            if value < minValue:
                minValue = minValue
                minDex = i
        return self.AStar(self.queue[minDex], goalNodeName, self.pathCosts[i],self.pathFuel[minDex])



    def TimeBetween(self, startID, endID):
        startTime = -1.0
        endTime = -1.0
        for i in range(self.instructionIndex,len(self.instructions)):
            if startTime == -1.0:
                if self.instructions[i][1] == startID:
                    startTime = self.instructions[i][2]
            
            if endTime == -1.0 and startTime != -1.0:
                if self.instructions[i][1] == endID:
                    endTime = self.instructions[i][2]
                    break
        
        return endTime - startTime
    

    def InsertPackageInteraction(self, interaction):
        index = 0
        for i in range(0,len(self.packageInteractions)):
            if self.packageInteractions[i][2] > interaction[2]:
                index = i
                break
        self.packageInteractions.insert(index,interaction)

            

    def InsertDelivery(self,packageID, pickupName, destinationName, t):
        #go through and insert pickup instruction
        ptime = t
        
        for i in range(self.instructionIndex, len(self.instructions)):
            if self.instructions[i][1] == pickupName:
                self.InsertPackageInteraction(("pickup", packageID, self.instructions[i][2]))

        #go through and insert dropoff instruction 
        if (self.ScheduledToVisitLocation(destinationName,t)):
            for i in range(self.instructionIndex, len(self.instructions)):
                if self.instructions[i][1] == destinationName:
                    self.InsertPackageInteraction(("dropoff", packageID, self.instructions[i][2]))
        else: #or schedule a dropoff instruction
            self.ScheduleDelivery(packageID,self.instructions[-1][1],destinationName, t)
            for inst in self.packageInteractions:
                if inst[1] == packageID and inst[0] == "pickup":
                    self.packageInteractions.remove(inst)
                    break
       



   