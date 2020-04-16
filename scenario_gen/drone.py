
import math
class Drone():
    def __init__(self, idCode, locationCode, packageCapacity, droneRange, scenario):
        self.idCode = idCode
        self.locationCode = locationCode
        self.packageCapacity = packageCapacity
        self.droneRange = droneRange
        self.droneFuel = droneRange
        self.scenario = scenario

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
        self.seenNodes = []
        self.queue = []
        self.pathCosts = []
        self.pathFuel = []
        self.savedDistances = dict()

        self.seenNodes.append(startNodeName)
        self.savedDistances[(startNodeName,startNodeName)] = 0
        return self.AStar([startNodeName],goalNodeName,0,self.droneFuel)

    
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
            return ([],-1)
        
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
   