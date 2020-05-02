from scenario import *
import numpy as np
import matplotlib.pyplot as plt

def PriorityPackage (package_list,max_carry):
 all_packages_p = []
 picked_packages = []
 count=0
 for i in package_list[:]:
  all_packages_p.append(i[3])
 #print(all_packages_p)
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

def Bidding (scenario,package_list,picked_packages,drone_debt,num_drones,drone_locations,drone_queue,dronepickup,dronedropoff,Dict1):
 time_entered=0
 time_delivered=0
 total_distance=0
 result = True;
 Costs = []
 drone_winnings =[[0]]*num_drones
 max_winnings = len(picked_packages)
 #print(picked_packages)
 for j in range(len(picked_packages)):
  element1 = picked_packages[j][1]
  element2 = picked_packages[j][2]
  for i in range(len(picked_packages)):
   if (element1 != picked_packages[i][1] or element2 != picked_packages[i][2]):
    result = False
 for j in range(len(picked_packages)):
  for i in range(num_drones):
   Drone = scenario.GetDrones()[i]
   Cost = Drone.GetPath(drone_locations[i],picked_packages[j][1])[1]
   Cost = Cost + Drone.GetPath(picked_packages[j][1],picked_packages[j][2])[1]
   Cost = Cost  + drone_debt[i]
   Costs.append(Cost)
  Winner = min(Costs)
  index_value = Costs.index(Winner)
  if (result == False):
   drone_winnings[index_value].append(picked_packages[j])
   drone_queue[index_value].append(picked_packages[j])
   dronepickup[index_value].append(picked_packages[j][1])
   dronedropoff[index_value].append(picked_packages[j][2])
   total_distance = Drone.GetPath(drone_locations[index_value],picked_packages[j][1])[1]+ Drone.GetPath(picked_packages[j][1],picked_packages[j][2])[1]
   time_delivered = drone_debt[index_value]+int(picked_packages[j][3])+ total_distance
   time_entered = drone_debt[index_value]+int(picked_packages[j][3])
   Dict1['totaldistance'][index_value] = Dict1['totaldistance'][index_value] + total_distance
   Dict1['jobs'][picked_packages[j][0]] = [time_entered,time_delivered,index_value]
   drone_debt[index_value] = Winner
   if len(picked_packages) == 1:
    drone_locations[index_value] = picked_packages[0][2]
   else:
    drone_locations[index_value] = picked_packages[j][2]
  #if maximum payload is at all one warehouse and destination, the drone who wins only pays one travel cost 
  if (result == True):
   #print("double")
   for j in range(len(picked_packages)):
    drone_winnings[index_value].append(picked_packages[j])
    drone_queue[index_value].append(picked_packages[j])
    dronepickup[index_value].append(picked_packages[j][1])
    dronedropoff[index_value].append(picked_packages[j][2])
   total_distance = Drone.GetPath(drone_locations[index_value],picked_packages[j][1])[1]+ Drone.GetPath(picked_packages[j][1],picked_packages[j][2])[1]
   drone_debt[index_value] = Winner
   time_delivered = drone_debt[index_value]+int(picked_packages[j][3])+ total_distance
   time_entered = drone_debt[index_value]+int(picked_packages[j][3])
   temp1 = int(drone_winnings[index_value][-1][3])
   temp2 = int(drone_winnings[index_value][1][3])
   Dict1['totaldistance'][index_value] = Dict1['totaldistance'][index_value] + total_distance
   Dict1['jobs'][picked_packages[j][0]] = [time_entered,time_delivered,index_value]
   drone_debt[index_value] = drone_debt[index_value]+ temp1 - temp2
   if len(picked_packages) == 1:
    drone_locations[index_value] = picked_packages[0][2]
   else:
    drone_locations[index_value] = picked_packages[j][2]
   
   break;
  Costs = []
 #print(drone_winnings)
 #if drone is under-loaded, check package request list for packages with same outbound. 
 for i in range(num_drones):
  if (len(drone_winnings[i]) <= len(picked_packages) and result != True):
   for j in range(len(package_list)):
    if(dronepickup[i][-1] == package_list[j][1]and dronedropoff[i][-1] == package_list[j][2] and(len(drone_winnings[i]) <= max_winnings+1)):
     drone_winnings[i].append(package_list[j])
     drone_queue[i].append(package_list[j])
     dronepickup[i].append(package_list[j][1])
     dronedropoff[i].append(package_list[j][2])
     temp1 = int(drone_winnings[i][-1][3])
     temp2 = int(drone_winnings[i][1][3])
     drone_debt[i] = drone_debt[i] + temp1 - temp2
     package_list.pop(j)
     break
 #print("Drone pickup 1 ",dronepickup[0]," ",dronepickup[1])
 #print("Drone dropoff 1 ",dronedropoff[0]," ",dronedropoff[1])
 #print("Dronel 1 ",drone_locations[0]," Dronel 2 ",drone_locations[1])
 #print("Dronec 1 ",drone_debt[0]," Dronec 2 ",drone_debt[1])
 #print("Droneq 1 ",drone_queue[0])
 #print("Droneq 2 ",drone_queue[1])
 #print("winnings: ",drone_winnings[0]," ",drone_winnings[1])
 return drone_debt,drone_locations,drone_queue,dronepickup,dronedropoff,package_list,Dict1

def Greedy(a,num_warhouses,num_dropoffs,num_drones,num_packages,fuelrange,max_carry):
 Dict1 = { 'totaldistance': { },'jobs':{}}
 index=0
 numpackages = len(a.GetRequests())
 picked_packages = []
 drone_locations = []
 drone_queue = [[]]*num_drones
 drone_pickup = [[]]*num_drones
 drone_dropoff = [[]]*num_drones
 drone_debt = [0]*num_drones
 package_list = []
 list_array2 = np.asarray(a.requestsList)
 for i in list_array2[:]:
  package_list.append(i)
 
 for i in range(num_drones):
  drone_locations.append(a.droneList[1].locationCode)
  Dict1['totaldistance'][i] = 0
 while(numpackages > 0):
 # print("iteration")
  picked_packages = PriorityPackage(package_list,max_carry)
  drone_debt, drone_locations,drone_queue,drone_pickup,drone_dropoff,package_list,Dict1 = Bidding(a,package_list,picked_packages,drone_debt,num_drones,drone_locations,drone_queue,drone_pickup,drone_dropoff,Dict1)
  numpackages = len(package_list)
  
 #diff = drone_debt[0] + drone_debt[1]+ drone_debt[2]
#print("Distance ",diff)
 #print("Drone 0 Debt",drone_debt[0])
 #print("Drone 1 Debt",drone_debt[1])
 #print("Drone 1 Debt",drone_debt[2])
 #print(Dict1['totaldistance'])
 #print(Dict1['jobs'])
 return Dict1['totaldistance'], Dict1['jobs']

 #print("Droneq 1 ",drone_queue[0])
 #print("Droneq 2 ",drone_queue[1])
#####################################################################

#Input Parameters for Greedy.py
num_warhouses = 1
num_dropoffs = 2
num_drones = 4
num_packages = 20
fuelrange = 3
max_carry = 2
a = Scenario(num_warhouses,num_dropoffs,num_drones,num_packages,fuelrange,max_carry)
a.PrintScenario()
Dict1,tec = Greedy(a,num_warhouses,num_dropoffs,num_drones,num_packages,fuelrange,max_carry)
######################################################################
 