#warehouses
#dropoffs
#droneNum
#requests
#drone range
from location import *
import random
import math
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

    def GenerateScenario(self):
        warehousesToPlace = self.wareHouseNum
        dropoffsToPlace = self.dropoffNum
        #generate warehouses and dropoffs
        self.warehouseList = []
        self.dropoffList = []
        self.droneList = []

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
                self.dropoffList.append(Location("D",len(self.warehouseList),px,py))

                dropoffsToPlace -= 1

        #place drones
        for i in range(0,self.droneNum):
            self.droneList.append(Drone(i, random.randint(0,len(self.warehouseList)-1), self.droneCapacity, self.droneRange)
)
    
    def PrintScenario(self):
        print("\n----------------------SCENARIO OVERVIEW----------------------\n")
        print("drone capacity: " + str(self.droneCapacity))
        print("drone range: " + str(self.droneRange))
        print("\nwarehouses------------")
        for w in self.warehouseList:
            print(" {i}, {x}, {y} ".format(i=w.idCode, x=w.x, y=w.y))
        print("\ndropoffs--------------")
        for d in self.dropoffList:
            print("( {i}, {x}, {y} )".format(i=d.idCode, x=d.x, y=d.y))
        print("\ndrones----------------")
        for r in self.droneList:
            print("( {i}, {wi}, {c}, {a} )".format(i = r.idCode, wi=r.locationCode, c = r.packageCapacity, a = r.droneRange))
 
        #place starting warehouse
        #place warehouses either within range of another warehouse, or within half range of dropoff position
        #palce dropoff positions within half range of warehouse


        #generate orders