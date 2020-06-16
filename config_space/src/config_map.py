#---Contains methods relating to configuration map------
#
# khaancc

# --- Imports ---
from PIL import Image, ImageDraw, ImagePath

from numpy import load
import numpy as np
import math
import matplotlib.pyplot as plt
from .formation import Formation as f
from .config_map_enlarger import enlarge
import copy

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely import affinity
from shapely.geometry import MultiPoint, MultiPolygon


# -- Output control --
log = True

# -- methods -- 
def create_config_space(formation,obstacles, boundary):
    if log:
        print("Started creating configuration space")
    # ---- Get config space boundary ----
    u = Polygon([(0.1,0.1),(0.1,boundary[1]-1.1),(boundary[0]-1.1,boundary[1]-1.1),(boundary[0]-1.1,0.1)])
    #Create empty config space
    cs = np.zeros([boundary[0],boundary[1]])
    count = 0
    for col in range(0,cs.shape[0]):
        print( math.floor(count/(cs.shape[0]*cs.shape[1])*100), "%" ,end="\r")
        for row in range(0, cs.shape[1]):
            
            in_bound = True
            collision = False
            #Check if in bounds
            formation.translate_to((row,col))
            exts = formation.get_points()
            for e in exts:
                if ( not Point(e).intersects(u)):
                    in_bound = False     
            #Check if collision
            if in_bound:
                for o in obstacles:
                    if formation.is_inside(o):
                        collision = True

            if not in_bound:
                cs[row][col] = 1
            if collision:
                cs[row][col] = 1

            
            """
            #plt.imshow(obstacles)
            xf, yf = zip(*formation.get_points())
            plt.plot(xf,yf,'-x')
            plt.pause(0.001)"""
            
            count += 1
            #formation.translate(1,0)              
        #formation.translate(-cs.shape[0],1)
    plt.show()
    return cs

def point2shape(points):
    output = []
    if log:
        print("Started point2shape process...")
    for row in range(0, points.shape[1]):
        for col in range(0, points.shape[0]):
            if points[row][col] > 0:
                output.append(Point(row, col))
    return output




if __name__ == "__main__":
    # execute only if run as a script
    #Example case
    plot = True

    p1 = Polygon([(2,4),(2,6),(4,6),(4,4)])
    p2 = Polygon([(10,10),(10,11),(11,11),(11,10)])
    obstacles = [Point(5,5),Point(15,15)]
    b = [20,20]  
    coords = [(0,0), (2,0), (0,2)]
    point= Point(5,5)
    d1 = f(coords)
    d1.rotate(-90)
    z = create_config_space(d1,obstacles,b)

    if plot:

        x = []
        y = []
        for tmp in range(0,b[1]):
            y.append(tmp)
        for tmp in range(0,b[0]):
            x.append(tmp)

        plt.imshow(z, cmap='Greys')

        plt.yticks(y)
        plt.xticks(x)
        plt.grid()
        plt.show()