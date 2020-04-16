import random
import math

import  matplotlib.pyplot as plt  
import networkx as nx
from location import *
from drone import *
class Scenario():
    def __init__(self,warehouseNum,dropNum,droneNum,requestNum,droneRange,droneCapacity):
        self.wareHouseNum = warehouseNum
        self.dropoffNum = dropNum
        self.droneNum = droneNum
        self.requestNum = requestNum
        self.droneRange = droneRange
        self.droneCapacity = droneCapacity
        self.GenerateScenario()
    
    def GetGraph(self):
        return self.graph

    def GetRequests(self):
        return self.requestsList

    def GetDrones(self):
        return self.droneList

    def GenerateScenario(self):
        warehousesToPlace = self.wareHouseNum
        dropoffsToPlace = self.dropoffNum
        
        #generate warehouses and dropoffs
        self.warehouseList = []
        self.dropoffList = []
        self.droneList = []
        self.requestsList = []

        #add first warehouse
        self.warehouseList.append(Location("W",0,0,0))
        
        while warehousesToPlace > 0 and dropoffsToPlace > 0:            

            #decide whether to place a warehouse or dropoff next
            warehouseOrDropoff = random.randint(1, dropoffsToPlace + warehousesToPlace - 1)
            placementAngle = random.uniform(0.0,365.0)
            if warehouseOrDropoff < warehousesToPlace:
                #find reference location 
                referenceLocationIndex = random.randint(0,len(self.warehouseList) + len(self.dropoffList) - 1)
                referenceLocation = self.warehouseList[0]
                if referenceLocationIndex < len(self.warehouseList):
                    referenceLocation = self.warehouseList[referenceLocationIndex]
                else:
                    referenceLocation = self.dropoffList[referenceLocationIndex - len(self.warehouseList)]
                
                #add a warehouse
                if referenceLocation.locationType is "W":
                    #place within drone range
                    radius = random.uniform(1.0, self.droneRange)
                    px = math.cos(placementAngle) * radius + referenceLocation.x
                    py = math.sin(placementAngle) * radius + referenceLocation.y
                    self.warehouseList.append(Location("W",len(self.warehouseList),px,py))
                else:
                    #place within half drone range
                    radius = random.uniform(1.0, self.droneRange / 2)
                    px = math.cos(placementAngle) * radius + referenceLocation.x
                    py = math.sin(placementAngle) * radius + referenceLocation.y
                    self.warehouseList.append(Location("W",len(self.warehouseList),px,py) )
                
                warehousesToPlace -= 1
            else:
                
                referenceLocation = self.warehouseList[random.randint(0,len(self.warehouseList)-1)]
                radius = random.uniform(1.0, self.droneRange / 2)
                px = math.cos(placementAngle) * radius + referenceLocation.x
                py = math.sin(placementAngle) * radius + referenceLocation.y
                self.dropoffList.append(Location("D",len(self.dropoffList),px,py))

                dropoffsToPlace -= 1

        #place drones
        for i in range(0,self.droneNum):
            self.droneList.append(Drone(i, random.randint(0,len(self.warehouseList)-1), self.droneCapacity, self.droneRange,self))
        
        #make requests
        deliverTime = 0
        for i in range(0, self.requestNum):
            self.requestsList.append((i, self.warehouseList[random.randint(0,len(self.warehouseList)-1)],self.dropoffList[random.randint(0,len(self.dropoffList)-1 )],deliverTime))
            deliverTime += random.randint(1,self.droneRange) 

        
        #make graph
        #add nodes
        nodes_list = []
        coords_list = []
        for w in self.warehouseList:
            nodes_list.append(w.idCode)
            coords_list.append((w.x,w.y))
        for d in self.dropoffList:
            nodes_list.append(d.idCode)
            coords_list.append((d.x,d.y))
        self.graph = nx.Graph()
        self.graph.add_nodes_from(nodes_list)
        
        self.positions = dict(zip(nodes_list,coords_list))

        #add edges - n^2 operation fix later lmaoooooooooo
        edges = []
        edgeWeights = []
        self.allLocations = []
        allLocations = (self.warehouseList) + (self.dropoffList)

        for loc in allLocations:
            for dest in allLocations:
                if loc != dest:
                    if self.DistBetweenLocs(loc, dest) <= self.droneRange:
                        self.graph.add_edge(loc.idCode,dest.idCode,weight = self.DistBetweenLocs(loc,dest))
                        edges.append((loc.idCode,dest.idCode))
                        edgeWeights.append(self.DistBetweenLocs(loc,dest))
            
        
        self.edgeWeightLabels = dict(zip(edges, edgeWeights))

    def DistBetweenLocs(self, loc1, loc2):
        return math.sqrt((loc2.x - loc1.x)*(loc2.x - loc1.x) + (loc2.y - loc1.y)*(loc2.y - loc1.y))

    
    def PrintScenario(self):
        print("\n----------------------SCENARIO OVERVIEW----------------------\n")
        print("drone capacity: " + str(self.droneCapacity))
        print("drone range: " + str(self.droneRange))
        print("\nwarehouses------------")
        for w in self.warehouseList:
            print("( {i}, {x}, {y} )".format(i=w.idCode, x=w.x, y=w.y))
        print("\ndropoffs--------------")
        for d in self.dropoffList:
            print("( {i}, {x}, {y} )".format(i=d.idCode, x=d.x, y=d.y))
        print("\ndrones----------------")
        for r in self.droneList:
            print("( {i}, {wi}, {c}, {a} )".format(i = r.idCode, wi=r.locationCode, c = r.packageCapacity, a = r.droneRange))
        print("\ndelivery requests----------")
        for q in self.requestsList:
            print("( {i}, {x}, {y}, {t} )".format(i=q[0], x=q[1].idCode, y=q[2].idCode, t=q[3]))
        #place starting warehouse
        #place warehouses either within range of another warehouse, or within half range of dropoff position
        #palce dropoff positions within half range of warehouse
        plt.figure(figsize=(20, 20))
        nx.draw_networkx(self.graph,self.positions)

        #generate orders
