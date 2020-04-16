# DroneDispatchProject
Hey Team, Code is still REAL messy right now but I'll try to keep the documentation updated here so you don't have to plunge into it.

**CLASSES**

The classes section has all the base objects, this includes the Scenario class which generates the problem, the Location class which can serve as a warehouse or dropoff, and the Drone class.


---


**Scenario Class Overview**

A new Scenario can be generated like so "a = Scenario(10,10,10,10,3,1)"
The constructor takes 6 parameters (wow so many). 
These parameters are (number of warehouses, number of dropoffs, number of drones, number of package orders, drone fuel range, max drone packages) in that order.

Here are some methods you can call from a scenario after it's generated

*   GetGraph() - returns the networkx graph for the problem
*   GetRequests() - returns list of package orders, each is a 4 tuple of (ID, origin, destination, time)
*   GetDrones() - returns list of drones
*   PrintScenario() - prints all info about scenario and a map


---



**Location Class Overview**

Not much to say, basically a struct containing location info. Locations have a type, either 'W' or 'D' depending on whether it's dropoff or warehouse. They contain their x, y coordinates, and an idCode (example: W0 for the first warehouseplaced, D0 for first dropoffplaced) **Nodes in the graph are labeled with the idCode of the Location they're meant to represent**

---

**Drone Class Overview**

Drone class need some work for evaluating answers later on. Right now it can "bid" on paths though. Drones are created when you make a scenario. Each has an idCode, locationCode, package capacity, and fuel range.

*   GetPath(startLocationName, endLocationName) - returns a tuple of list of nodes (id codes) in shortest path, and the length of that path. These paths take fuel into consideration. A drone will not take a path which expends all of its fuel







