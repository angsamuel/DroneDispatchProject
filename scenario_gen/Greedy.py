from scenario import *
import numpy as np
import matplotlib.pyplot as plt
#(number of warehouses, number of dropoffs, number of drones, 
#number of package orders, drone fuel range, max drone packages)

def PriorityPackage (self,max_carry):
 all_packages_p = []
 picked_packages = []
 count=0
 list_array = np.asarray(self.requestsList)
 #for q in self.requestsList:
  #print("self requests ( {i}, {x}, {y}, {t} )".format(i=q[0], x=q[1].idCode, y=q[2].idCode, t=q[3]))
 for i in list_array:
  all_packages_p.append(i[3])
 for i in range(max_carry):
  #print("all packages ",all_packages_p)
  pick = min(all_packages_p)
  index_value = all_packages_p.index(pick)
  del all_packages_p[index_value]
  index_value = index_value+count
  #print("requestList ( {i}, {x}, {y}, {t} )".format(i=self.requestsList[index_value][0], x=self.requestsList[index_value][1].idCode, y=self.requestsList[index_value][2].idCode, t=self.requestsList[index_value][3]))
  picked_packages.append(self.requestsList[index_value])
  
  count = count+1
 #print("picked packages ",picked_packages[0][2].idCode," ",picked_packages[1][2].idCode)
 return picked_packages

def Bidding (self,picked_packages,drone_debt,num_drones,drone_locations,drone_queue):
 Drones = []
 Costs = []
 for j in range(len(picked_packages)):
  for i in range(num_drones):
   Drone = a.GetDrones()[i]
   Cost = Drone.GetPath(drone_locations[i].idCode,picked_packages[j][1].idCode)[1]
   Cost = Cost + Drone.GetPath(picked_packages[j][1].idCode,picked_packages[j][2].idCode)[1]
   Cost = Cost   + drone_debt[i]
   Costs.append(Cost)
  Winner = min(Costs)
  index_value = Costs.index(Winner)
  drone_debt[index_value] = Winner
  drone_queue[index_value].append(picked_packages[j][2].idCode)
  drone_locations[index_value] = picked_packages[i][2]
  Costs = []
 #print(picked_packages[0][2].idCode," ",picked_packages[1][2].idCode)
 return drone_debt,drone_locations,drone_queue

num_warhouses = 2
num_dropoffs = 6
num_drones = 2
num_packages = 4000
fuelrange = 3
max_carry = 2

a = Scenario(num_warhouses,num_dropoffs,num_drones,num_packages,fuelrange,max_carry)

#################
wlist = ['W0','W1']
dlist = ['D0','D1','D2','D3','D4','D5']
d1sum=0
d2sum=0
Drone = a.GetDrones()[0]
'''
for i in range(len(wlist)):
 for j in range(len(dlist)):
  print("Distance ",wlist[i]," ",dlist[j]," ",Drone.GetPath(wlist[i],dlist[j])[1])
  if (a.warehouseList[i].idCode == wlist[i]  and a.dropoffList[i].idCode == dlist[i] and i ==0):
   d1sum = d1sum + Drone.GetPath(wlist[i],dlist[j])[1]
  if (a.warehouseList[i].idCode == wlist[i]  and a.dropoffList[i].idCode == dlist[i] and i ==1):
   d2sum = d2sum + Drone.GetPath(wlist[i],dlist[j])[1]
   '''
for i in range(len(a.GetRequests())):
 if (a.requestsList[i][1].idCode == 'W0'):
   d1sum = d1sum + Drone.GetPath('W0',a.requestsList[i][2].idCode)[1]
 if (a.requestsList[i][1].idCode == 'W1'):
   d2sum = d2sum + Drone.GetPath('W1',a.requestsList[i][2].idCode)[1]
print("Drone1 ",d1sum*2)
print("Drone2 ",d2sum*2)
##################

numpackages = len(a.GetRequests())
picked_packages = []
drone_locations = []
drone_queue = [[0],[0]]
drone_debt = [0]*num_drones

for i in range(num_drones):
 drone_locations.append(a.warehouseList[i])
#a.PrintScenario()
while(numpackages > 0):
 #print("iterlation")
 picked_packages = PriorityPackage(a,max_carry)
 drone_debt, drone_locations,drone_queue = Bidding(a,picked_packages,drone_debt,num_drones,drone_locations,drone_queue)
 numpackages = numpackages - 2
 for i in range(num_drones):
  a = a.Remove(0)
 #print("Drone Debt: ",drone_debt)
 #print("Drone Queue",drone_queue)
sum = d1sum*2+d2sum*2
print("n sum ",sum)
print("Difference")
diff = drone_debt[0] + drone_debt[1] - sum
print(diff)
#nx.draw(a.GetGraph())
#plt.show()
