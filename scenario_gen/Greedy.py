from scenario import *
import numpy as np
import matplotlib.pyplot as plt

def PriorityPackage (package_list,max_carry):
 all_packages_p = []
 picked_packages = []
 count=0
 for i in package_list[:]:
  all_packages_p.append(i[3])
 print(all_packages_p)
 if len(package_list) >= max_carry:
  for i in range(max_carry):
   pick = min(all_packages_p)
   index_value = all_packages_p.index(pick)
   del all_packages_p[index_value]
   index_value = index_value+count
   picked_packages.append(package_list[index_value])
   count = count+1
  for i in range(max_carry):
   package_list.pop(0)
 elif len(package_list) < max_carry:
  for i in range(len(package_list)):
   pick = min(all_packages_p)
   index_value = all_packages_p.index(pick)
   del all_packages_p[index_value]
   index_value = index_value+count
   picked_packages.append(package_list[index_value])
   count = count+1
  for i in range(len(package_list)):
   package_list.pop(0)
 return picked_packages

def Bidding (package_list,picked_packages,drone_debt,num_drones,drone_locations,drone_queue,dronepickup,dronedropoff):
 result = True;
 Costs = []
 drone_winnings =[[0],[0]]
 max_winnings = len(picked_packages)
 for j in range(len(picked_packages)):
  element1 = picked_packages[j][1].idCode
  element2 = picked_packages[j][2].idCode
  for i in range(len(picked_packages)):
   if (element1 != picked_packages[i][1].idCode or element2 != picked_packages[i][2].idCode):
    result = False
 for j in range(len(picked_packages)):
  for i in range(num_drones):
   Drone = a.GetDrones()[i]
   Cost = Drone.GetPath(drone_locations[i].idCode,picked_packages[j][1].idCode)[1]
   Cost = Cost + Drone.GetPath(picked_packages[j][1].idCode,picked_packages[j][2].idCode)[1]
   Cost = Cost  + drone_debt[i]
   Costs.append(Cost)
  Winner = min(Costs)
  index_value = Costs.index(Winner)
  if (result == False):
   drone_winnings[index_value].append(picked_packages[j])
   drone_queue[index_value].append(picked_packages[j])
   dronepickup[index_value].append(picked_packages[j][1].idCode)
   dronedropoff[index_value].append(picked_packages[j][2].idCode)
   drone_debt[index_value] = Winner
   drone_locations[index_value] = picked_packages[index_value][2]
   
  #if maximum payload is at all one warehouse and destination, the drone who wins only pays one travel cost 
  if (result == True):
   #print("double")
   for j in range(len(picked_packages)):
    drone_winnings[index_value].append(picked_packages[j])
    drone_queue[index_value].append(picked_packages[j])
    dronepickup[index_value].append(picked_packages[j][1].idCode)
    dronedropoff[index_value].append(picked_packages[j][2].idCode)
   drone_debt[index_value] = Winner
   drone_locations[index_value] = picked_packages[index_value][2]
   break;
  Costs = []
 #print(drone_winnings)
 #if drone is under-loaded, check package request list for packages with same outbound. 
 for i in range(num_drones):
  if (len(drone_winnings[i]) <= len(picked_packages) and result != True):
   for j in range(len(package_list)):
    if(dronepickup[i][-1] == package_list[j][1].idCode and dronedropoff[i][-1] == package_list[j][2].idCode and(len(drone_winnings[i]) < max_winnings+1)):
     drone_winnings[index_value].append(package_list[j])
     drone_queue[index_value].append(package_list[j])
     dronepickup[index_value].append(package_list[j][1].idCode)
     dronedropoff[index_value].append(package_list[j][2].idCode)
     package_list.pop(j)
     break
 #print("Drone pickup 1 ",dronepickup[0]," ",dronepickup[1])
 #print("Drone dropoff 1 ",dronedropoff[0]," ",dronedropoff[1])
 #print("Dronel 1 ",drone_locations[0].idCode," Dronel 2 ",drone_locations[1].idCode)
 #print("Dronec 1 ",drone_debt[0]," Dronec 2 ",drone_debt[1])
 #print("Droneq 1 ",drone_queue[0])
 #print("Droneq 2 ",drone_queue[1])
 #print("winnings: ",drone_winnings[0]," ",drone_winnings[1])
 return drone_debt,drone_locations,drone_queue,dronepickup,dronedropoff,package_list

num_warhouses = 2
num_dropoffs = 2
num_drones = 2
num_packages = 10
fuelrange = 3
max_carry = 3
index=0
a = Scenario(num_warhouses,num_dropoffs,num_drones,num_packages,fuelrange,max_carry)
a.PrintScenario()

numpackages = len(a.GetRequests())
picked_packages = []
drone_locations = []
drone_queue = [[],[]]
drone_pickup = [[0],[0]]
drone_dropoff = [[0],[0]]
drone_debt = [0]*num_drones
package_list = []
list_array2 = np.asarray(a.requestsList)
for i in list_array2[:]:
 package_list.append(i)
for i in range(num_drones):
 drone_locations.append(a.warehouseList[i])
while(numpackages > 0):
 picked_packages = PriorityPackage(package_list,max_carry)
 drone_debt, drone_locations,drone_queue,drone_pickup,drone_dropoff,package_list = Bidding(package_list,picked_packages,drone_debt,num_drones,drone_locations,drone_queue,drone_pickup,drone_dropoff)
 numpackages = len(package_list)
  
diff = drone_debt[0] + drone_debt[1]
print("Distance ",diff)