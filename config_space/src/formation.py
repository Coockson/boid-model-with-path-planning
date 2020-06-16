from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely import affinity
import numpy as np
import math
import matplotlib.pyplot as plt

class Formation:

    def __init__(self, points):
        self.polygon = Polygon(points)

    def rotate(self, deg):
        self.polygon = affinity.rotate(self.polygon, angle=deg, origin=(0,0), use_radians=False)

    def get_points(self):
        return list(self.polygon.exterior.coords)

    def is_inside(self, point):
        return (point.intersects(self.polygon) or self.polygon.within(point) or self.polygon.touches(point))

    def get_boundary(self):
        return list(self.polygon.bounds)  #(minx, miny, maxx, maxy)

    def translate(self,x,y):
        self.polygon = affinity.translate(self.polygon, xoff=x,yoff=y)

    def translate_to(self, point):
        current = self.get_points()[0]
        self.translate(point[0]-current[0],point[1]-current[1])

    def mirror(self):
        bounds = self.get_boundary()
        self.polygon= affinity.scale(self.polygon, yfact=-1, origin=(0,bounds[3]))

    def face_to(self, point):
        sensitivity = 10
        for i in range(0, int(math.floor(360/sensitivity))):
            count = 0
            face_forward = False
            shortest = math.inf
            for x in self.get_points()[1:-1]:
                print(self.__get_dist__(self.get_points()[0],point))
                print(self.__get_dist__(x,point))
                print("----")
                if self.__get_dist__(x,point)> self.__get_dist__(self.get_points()[0],point):
                    count += 1
            
            if count == len(self.get_points()[1:-1]):
                if self.__get_dist__(self.get_points()[0],point)< shortest:
                    shortest = self.__get_dist__(self.get_points()[0],point)
                else:
                    self.rotate(-sensitivity)
                    break
            else:
                self.rotate(sensitivity)


    #Private methods
    def __get_dist__(self, a, b):
        return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)


    #Extra
    def area(self):
        print(self.polygon.area)

    