from lib.boids.boids import BoidModel
from lib.path.a_star import AStarPlanner
from lib.path.rrt_star import RRTStar
from tkinter import *
from tkinter import ttk
import numpy as np
import argparse
TK_SILENCE_DEPRECATION=1
parser = argparse.ArgumentParser()

parser.add_argument("cs", help="Path to the configuration space", type=str)
parser.add_argument("start", help="Start point. \"x,y\" , e.g \"10,10\" ", type=str)
parser.add_argument("goal", help="Goal point. \"x,y\" , e.g \"10,10\" ", type=str)
parser.add_argument("--path", help="The path planning algorithm. E.g \"a*\" or \"rrt*\"  ", type=str)
parser.add_argument("--droneInit", help="Drone start location. \"x,y\" , Default \"0,0\" ", type=str)
parser.add_argument("--droneSpread", help="Drone spread around initial point. Default 5 ", type=int)
parser.add_argument("--aStarReso", help="A* algorithm resolution. Default 5 ", type=int)


args = parser.parse_args()

cs = np.load(args.cs)
start = [int(x) for x in (str(args.start)).split(",")]
goal = [int(x) for x in (str(args.goal)).split(",")]
selection = 1
init = [0,0]
spread = 5
areso = 5

if args.path:
    if args.path == "a*":
        selection = 1
    if args.path == "rrt*":
        selection = 2

if args.droneInit:
    init = [int(x) for x in (str(args.droneInit)).split(",")]

if args.droneSpread:
    spread = args.droneSpread

if args.aStarReso:
    areso = args.aStarReso

#temp data
cs = np.zeros([500,500])
cs[1][1] = 1
cs[499][0] = 1
cs[0][499] = 1
cs[499][499] = 1
cs[250:300,0:230] = 1
cs[250:300,270:500] = 1
#path = [(200,250),(420,250),(500,10)]


#=======================================================================
if selection == 1:
    print("Started A* path planning")
    ox = []
    oy = []
    for row in range(cs.shape[0]-1,0,-1):
        for col in range(0,cs.shape[1]):
            if(cs[row][col]>0):
                ox.append(row)
                oy.append(col)
    print(start, goal)
    planner = AStarPlanner(ox,oy,areso,1)
    pathx, pathy = planner.planning(start[0],start[1],goal[0],goal[1])
    path = list(zip(pathx,pathy))
    path.reverse()
    print("Path planning done")
if selection == 2:
    print("Started RRT* path planning")
    newcs = []
    for row in range(0,cs.shape[0]):
        for col in range(0,cs.shape[1]):
            if(cs[row][col]>0):
                newcs.append((row,col,1))

    rrt_star = RRTStar(     start=[start[0], start[1]],
                            goal=[goal[0], goal[1]],
                            rand_area=[-2, 100],
                            obstacle_list=newcs)
    path = rrt_star.planning(animation=False)
    print("Path planning done")
#=======================================================================





a = BoidModel(0.12, 0.30,  0.05, 0.05,   0.08,  50,  4, 3, 5, 20,  cs,path,init,spread)
a.runBoid()
