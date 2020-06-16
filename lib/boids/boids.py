import math
import random
import numpy as np
import copy
from tkinter import * 
from tkinter import ttk
import time
import sys
import os

debug = False


class BoidModel():

    def __init__(self,centeringFactor,avoidFactor,matchingFactor ,avoidFactorObs,motivation,goalDist,minDistance,speedLimit,numBoids, visualRange, cs, path,init,spread):
        self.centeringFactor =centeringFactor 
        self.avoidFactor= avoidFactor 
        self.avoidFactorObs = avoidFactorObs 
        self.motivation = motivation 
        self.goalDist = goalDist 
        self.minDistance = minDistance 
        self.speedLimit = speedLimit 
        self.numBoids = numBoids 
        self.visualRange = visualRange
        self.cs = cs
        self.path = path
        self.matchingFactor = matchingFactor
        self.init = init
        self.spread = spread

        self.width = cs.shape[0]
        self.height = cs.shape[1]
        self.boids = []
        self.dummy_boids = []

        self.experiment = []
        self.done = False
        self.master = Tk() 
        self.pause = False

        self.col_drone = 0
        self.col_obs = 0

        #self.broken = broken

        self.show = True
        self.calcCol = True

    """numBoids =8
    visualRange = 50  #75  # possible idea: change visual range to formation shape 

    centeringFactor = 0.02 #0.005  #Coherence Each boid flies towards the the other boids.
    avoidFactor = 0.8 #0.15 # Adjust velocity by this  If it gets too close to another boid it will steer away from it
    avoidFactorObs = 0.2
    motivation = 0.08
    goalDist = 20
    minDistance = 4
    speedLimit = 10"""

    """boids = []
    dummy_boids = []"""


    class Boid():
        def __init__(self, ID, x, y):
            self.ID = ID 
            self.x = x
            self.y = y
            self.dx = random.random() * 10 - 5
            self.dy = random.random() * 10 - 5
            self.history = []
            self.waypoint = 0


    def initBoids(self):

        for i in range(0, self.numBoids): 
            self.boids.append(BoidModel.Boid(i,random.random() *self.spread+self.init[0], random.random() *self.spread+self.init[1]))

    def distance(self,a, b):
        return np.sqrt((b.x - a.x) ** 2 + (b.y - a.y) ** 2)

    def nClosestBoids(self,boid, n):
        self.boids
        temp = copy.deepcopy(self.boids)
        dists = []
        for a in temp:
            dists.append(self.distance(boid,a))
        
        k = [x for _,x in sorted(zip(dists,temp))]
        return k[1:n+1]

    def keepWithinBounds(self,boid):
        margin = 1
        turnFactor = 4
        if (boid.x < margin):
            boid.dx += turnFactor
        
        if (boid.x > self.width - margin):
            boid.dx -= turnFactor
        
        if (boid.y < margin):
            boid.dy += turnFactor
        
        if (boid.y > self.height - margin):
            boid.dy -= turnFactor

    def flyTowardsCenter(self,boid):


        centerX = 0
        centerY = 0
        numNeighbors = 0

#        if boid.ID in self.broken:
#            for otherBoid in self.boids:
#                if (self.distance(boid, otherBoid) < 1):
#                    centerX += otherBoid.x
#                    centerY += otherBoid.y
#                    numNeighbors += 1
        
        for otherBoid in self.boids:
            if (self.distance(boid, otherBoid) < self.visualRange):
                centerX += otherBoid.x
                centerY += otherBoid.y
                numNeighbors += 1

        if (numNeighbors):
            centerX = centerX / numNeighbors
            centerY = centerY / numNeighbors

            boid.dx += (centerX - boid.x) * self.centeringFactor
            boid.dy += (centerY - boid.y) * self.centeringFactor
        
    def avoidOthers(self,boid):

        
        moveX = 0
        moveY = 0


        for otherBoid in self.boids:
            if (otherBoid != boid):
                if (self.distance(boid, otherBoid) < self.minDistance and self.distance(boid, otherBoid)< self.visualRange):
                    moveX += boid.x - otherBoid.x
                    moveY += boid.y - otherBoid.y

        boid.dx += moveX * self.avoidFactor
        boid.dy += moveY * self.avoidFactor

    def matchVelocity(self,boid):


        avgDX = 0
        avgDY = 0
        numNeighbors = 0

        for otherBoid in self.boids:
            if (self.distance(boid, otherBoid) < self.visualRange):
                avgDX += otherBoid.dx
                avgDY += otherBoid.dy
                numNeighbors += 1

        if (numNeighbors):
            avgDX = avgDX / numNeighbors
            avgDY = avgDY / numNeighbors

            boid.dx += (avgDX - boid.dx) * self.matchingFactor
            boid.dy += (avgDY - boid.dy) * self.matchingFactor

    def limitSpeed(self,boid):


        speed = math.sqrt(boid.dx * boid.dx + boid.dy * boid.dy)
        if (speed > self.speedLimit):
            boid.dx = (boid.dx / speed) * self.speedLimit
            boid.dy = (boid.dy / speed) * self.speedLimit

    def add_obstacle(self):

        for xi in range(0, self.cs.shape[0]):
            for yi in range(0, self.cs.shape[1]):
                if self.cs[xi][yi] == 1:
                    self.dummy_boids.append(BoidModel.Boid(-1,xi,yi))

    def avoidObsticles(self,boid):
        self.dummy_boids
        self.avoidFactorObs
        minDistance = 12 # The distance to stay away from other boids
        
        moveX = 0
        moveY = 0

        for otherBoid in self.dummy_boids:
            if (self.distance(boid, otherBoid) < minDistance and self.distance(boid, otherBoid)< self.visualRange):
                moveX += boid.x - otherBoid.x
                moveY += boid.y - otherBoid.y

        boid.dx += moveX * self.avoidFactorObs
        boid.dy += moveY * self.avoidFactorObs
    """
    def towardsGoal(boid):
        self.goal
        self.motivation
        boid.dx += (goal[0] - boid.x) * motivation
        boid.dy += (goal[1] - boid.x) * motivation"""

    def followPath(self,boid, path,count):
        current = boid.waypoint


        if(np.sqrt((path[current][0] - boid.x) ** 2 + (path[current][1] - boid.y) ** 2) < self.goalDist):
            if debug:
                print("Boid", boid.ID, " reched waypoint ", current, "Iteration:", count)
                #check all
                print(len(self.experiment), len(path), self.experiment)
            if(len(path)-1==current):
                attended = []
                for i in self.experiment:
                    attended.append(i[0])
                if boid.ID not in attended:
                    self.experiment.append((boid.ID,count))
                boid.dx = 0
                boid.dy = 0
            if(len(path)-1!=current):
                
                boid.waypoint += 1
            if(len(self.experiment)==self.numBoids):
                self.done = True
        if(len(path)!=current):
            boid.dx += (path[current][0] - boid.x) * self.motivation
            boid.dy += (path[current][1] - boid.y) * self.motivation
    
    def results(self):
        #print("--- Experiment results ---")
        self.master.destroy()
        return [(self.col_drone/2)+self.col_obs,len(self.experiment),self.experiment]
    # -------- Animate ------------------------
    

    def runBoid(self):

        

        control = Frame(self.master)

        cohlbl = Label(control,text="Coherence",padx=10)
        cohlbl.grid(row=0,column=1,sticky=W)
        v = StringVar(control, value=str(self.centeringFactor))
        coh = Entry(control,width=8, textvariable= v)
        coh.grid(row=1,column=1,sticky=W,padx=10)

        seplbl = Label(control,text="Seperation",padx=10)
        seplbl.grid(row=0,column=2,sticky=W)
        v = StringVar(control, value=str(self.avoidFactor))
        sep = Entry(control,width=8, textvariable= v)
        sep.grid(row=1,column=2,sticky=W,padx=10)

        alilbl = Label(control,text="Alignment",padx=10)
        alilbl.grid(row=0,column=3,sticky=W)
        v = StringVar(control, value=str(self.matchingFactor))
        ali = Entry(control,width=8, textvariable= v)
        ali.grid(row=1,column=3,sticky=W,padx=10)

        goallbl = Label(control,text="Follow goal",padx=10)
        goallbl.grid(row=0,column=4,sticky=W)
        v = StringVar(control, value=str(self.motivation))
        goal = Entry(control,width=8, textvariable= v)
        goal.grid(row=1,column=4,sticky=W,padx=10)

        goaldlbl = Label(control,text="Goal dist.",padx=10)
        goaldlbl.grid(row=0,column=5,sticky=W)
        v = StringVar(control, value=str(self.goalDist))
        goald = Entry(control,width=8, textvariable= v)
        goald.grid(row=1,column=5,sticky=W,padx=10)

        mindlbl = Label(control,text="Minimum dist.",padx=10)
        mindlbl.grid(row=0,column=6,sticky=W)
        v = StringVar(control, value=str(self.minDistance))
        mind = Entry(control,width=8, textvariable= v)
        mind.grid(row=1,column=6,sticky=W,padx=10)

        vrlbl = Label(control,text="Visual dist.",padx=10)
        vrlbl.grid(row=0,column=7,sticky=W)
        v = StringVar(control, value=str(self.visualRange))
        vr = Entry(control,width=8, textvariable= v)
        vr.grid(row=1,column=7,sticky=W,padx=10)
        
        numlbl = Label(control,text="Collisions:",padx=10)
        numlbl.grid(row=2,column=5,sticky=W)
        strlbl = StringVar()
        strlbl.set(str(self.col_drone/2+self.col_obs))
        colLabel = Label(control,text=strlbl.get(),padx=10)
        colLabel.grid(row=2,column=6,sticky=W,padx=10)
        

        def getClick():
            if not (len(coh.get())) == 0:
                self.centeringFactor = float(coh.get())
            if not (len(mind.get()) == 0):    
                self.minDistance = int(mind.get())
            if not (len(goald.get()) == 0):    
                self.goalDist = int(goald.get())
            if not (len(vr.get()) == 0):    
                self.visualRange = int(vr.get())
            if not (len(sep.get()) == 0):    
                self.avoidFactor = float(sep.get())
            if not (len(ali.get()) == 0):    
                self.matchingFactor = float(ali.get())
            if not (len(goal.get()) == 0):    
                self.motivation = float(goal.get())
            

        def startClick():
            self.pause = not self.pause

        def restart_program():
            """Restarts the current program.
            Note: this function does not return. Any cleanup action (like
            saving data) must be done before calling this function."""
            python = sys.executable
            os.execl(python, python, * sys.argv)

        """def updateCollision():
            print("Collision!")
            strlbl.set(str(self.col_drone/2+self.col_obs))"""

        getButton = ttk.Button(control, text = "Apply",command= getClick)
        getButton.grid(row=2,column=1,sticky=W)

        startButton = ttk.Button(control, text = "Stop",command= startClick)
        startButton.grid(row=2,column=2,sticky=W)

        resButton = ttk.Button(control, text = "Restart",command= restart_program)
        resButton.grid(row=2,column=3,sticky=W)

        control.pack(padx=1,pady=1)

        if self.show:
            self.master.title("Swarm Simulator")
            canvas = Canvas(self.master, width=self.width, height=self.height)
            canvas.pack(expand=YES, fill=BOTH)
        
        """def paint(self,boid):
            self.canvas
            python_green = "#476042"
            x1, y1 = (self.boid.x - 1), (self.boid.y - 1)
            x2, y2 = (self.boid.x + 1), (self.boid.y + 1)
            return canvas.create_rectangle(x1, y1,x2, y2)
            #return canvas.create_line(boid.x, boid.y,boid.x + 1, boid.y)"""

        self.initBoids()
        self.add_obstacle()

        if self.show:
            for obs in self.dummy_boids:
                python_green = "#476042"
                x1, y1 = (obs.x - 1), (obs.y - 1)
                x2, y2 = (obs.x + 1), (obs.y + 1)
                canvas.create_rectangle(x1, y1, x2, y2, fill=python_green)

            for obs in self.path:
                x1, y1 = (obs[0] - 1), (obs[1] - 1)
                x2, y2 = (obs[0] + 1), (obs[1] + 1)
                blue = "#1303fc"
                canvas.create_rectangle(x1, y1, x2, y2, fill= blue)



            to_paint = [None] * self.numBoids

            count = 0
            for boid in self.boids[0:self.numBoids]:
                x1, y1 = (boid.x - 1), (boid.y - 1)
                x2, y2 = (boid.x + 1), (boid.y + 1)
                to_paint[count] = canvas.create_rectangle(x1, y1,x2, y2)
                boid.history.append([boid.x,boid.y])
                count += 1
        
        iteration = 0
        while self.done == False: #and iteration < 1500:
            if not self.pause:
                count = 0
                for boid in self.boids[0:self.numBoids]:
                    # Update the velocities according to each rule
                    
                    self.avoidObsticles(boid)
                    self.flyTowardsCenter(boid)
                    self.followPath(boid, self.path,iteration)
                    self.matchVelocity(boid)
                    self.limitSpeed(boid)
                    self.keepWithinBounds(boid)
                    
                    self.avoidOthers(boid)
                    
                    # Update the position based on the current velocity
                    boid.x += boid.dx
                    boid.y += boid.dy
                    
                    if self.show:
                        canvas.create_line(boid.history[-1][0], boid.history[-1][1],boid.x, boid.y)
                        boid.history.append([boid.x, boid.y])
                        #boid.history = boid.history.slice(-50)
                    
                    canvas.move(to_paint[count],boid.dx,boid.dy )
                    count += 1
                    iteration += 1
                    if self.show:
                        time.sleep(0)
                    
                    if self.calcCol:
                        if count == self.numBoids:
                            for boid in self.boids:
                                for other in self.boids:
                                    if (boid!= other and boid.waypoint < len(self.path) and other.waypoint < len(self.path)-1 
                                        and boid.waypoint != 0 and other.waypoint != 0):
                                        if (    math.sqrt((boid.x-other.x)**2 + (boid.y-other.y)**2) < 1 ):
                                            self.col_drone = self.col_drone +1
                                            #updateCollision()
                                            print("Collision!")
                                            strlbl.set(str(self.col_drone/2+self.col_obs))
                            for boid in self.boids:
                                for obs in self.dummy_boids:
                                    if ( boid.waypoint < len(self.path) and other.waypoint < len(self.path)-1 
                                        and boid.waypoint != 0 and other.waypoint != 0):
                                        if (    math.sqrt((boid.x-obs.x)**2 + (boid.y-obs.y)**2) < 1 ):
                                            self.col_obs = self.col_obs +1
                                            #updateCollision()
                                            print("Collision!")
                                            strlbl.set(str(self.col_drone/2+self.col_obs))
                            
                    
                    if self.show:
                        self.master.update_idletasks()
                        self.master.update()
                else:
                    time.sleep(0.2)
                    pass
        self.master.mainloop()
            
            

