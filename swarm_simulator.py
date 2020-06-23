from lib.boids.boids import BoidModel
from lib.path.a_star import AStarPlanner
from lib.path.rrt_star import RRTStar
from tkinter import *
from tkinter import ttk
import numpy as np
import argparse


parser = argparse.ArgumentParser()

parser.add_argument("--cs", help="Path to the configuration space", type=str)
parser.add_argument("--start", help="Start point. \"x,y\" , e.g \"10,10\" ", type=str)
parser.add_argument("--goal", help="Goal point. \"x,y\" , e.g \"10,10\" ", type=str)
parser.add_argument("--numDrones", help="Number of drones. Default 5 ", type=int)
parser.add_argument("--expath", help="example paths ", type=int)
parser.add_argument("--exmap", help="example maps ", type=int)
parser.add_argument("--tail", help="Drone trail. 1 enabled, 2 disabled ", type=int)
parser.add_argument("--path", help="The path planning algorithm. E.g \"a*\" or \"rrt*\"  ", type=str)
parser.add_argument("--droneInit", help="Drone start location. \"x,y\" , Default \"0,0\" ", type=str)
parser.add_argument("--droneSpread", help="Drone spread around initial point. Default 5 ", type=int)
parser.add_argument("--aStarReso", help="A* algorithm resolution. Default 5 ", type=int)


args = parser.parse_args()
if args.cs:
    cs = np.load(args.cs)

if args.start:
    start = [int(x) for x in (str(args.start)).split(",")]

if args.goal:
    goal = [int(x) for x in (str(args.goal)).split(",")]
selection = 1
init = [0,0]
spread = 5
areso = 5

tail = 1
if args.tail:
    tail = args.tail

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

numDrones = 5
if args.numDrones:
    numDrones = args.numDrones

exmap = 1
if args.exmap:
    exmap = args.exmap

expath = 1
if args.expath:
    expath = args.expath

if exmap == 1:
    cs = np.zeros([500,500])
    cs[50:150,50:150] = 1
    cs[300:400,300:400] = 1
    cs[200:250,100:300] = 1

if expath == 1:
    path = [(20,100),(40,200),(160,200),(180,130),(220,70),(270,130), (270,250)]

if expath == 2:
    path = [(20,100),(160,200),(270,130)]

if exmap == 2:
    cs = np.zeros([500,500])
    cs[1][1] = 1
    cs[499][0] = 1
    cs[0][499] = 1
    cs[499][499] = 1
    cs[250:300,0:230] = 1
    cs[250:300,270:500] = 1
    path = [(100,150),(200,250),(420,250),(500,10)]





#=======================================================================
if selection == 1 and args.path:
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
if selection == 2 and args.path:
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





a = BoidModel(0.12, 0.30,  0.05, 0.05,   0.02,  20,  4, 4, numDrones, 20,  cs,path,init,spread,tail)
a.runBoid()
