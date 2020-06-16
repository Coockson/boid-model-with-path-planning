from numpy import load
import matplotlib.pyplot as plt
import argparse
import copy
import numpy as np

def enlarge(name, delta, scale_min):
    data = load('lib/config_space/data_dir/'+ name +'.npy')
    

    scaled = data[scale_min:2500]
    scaled = np.delete(scaled, np.s_[0:scale_min],1)

    tempData = copy.deepcopy(scaled)
    enlarged = copy.deepcopy(scaled)

    y_max = scaled.shape[1]-1
    x_max = scaled.shape[0]-1

    for i in range(0,delta):
        print("Enlarged by ", i+1)
        for (x, y), value in np.ndenumerate(tempData):
            if(value <= 0):
                if x > 0 and y < y_max-1 and x<x_max-1:
                    enlarged[x-1][y+1] = 0
                    enlarged[x][y+1] = 0
                    enlarged[x+1][y+1] = 0
                    enlarged[x-1][y] = 0
                    enlarged[x+1][y] = 0
                    enlarged[x-1][y-1] = 0
                    enlarged[x][y-1] = 0
                    enlarged[x+1][y-1] = 0
        tempData=copy.deepcopy(enlarged)

    return enlarged

def enlargecs(cs, delta):
    tempData = copy.deepcopy(cs)
    enlarged = copy.deepcopy(cs)
    y_max = enlarged.shape[1]-1
    x_max = enlarged.shape[0]-1
    for i in range(0,delta):
        print("Enlarged by ", i+1)
        for (x, y), value in np.ndenumerate(tempData):
            if(value == 1):
                if x > 0 and y < y_max-1 and x<x_max-1:
                    enlarged[x-1][y+1] = 1
                    enlarged[x][y+1] = 1
                    enlarged[x+1][y+1] = 1
                    enlarged[x-1][y] = 1
                    enlarged[x+1][y] = 1
                    enlarged[x-1][y-1] = 1
                    enlarged[x][y-1] = 1
                    enlarged[x+1][y-1] = 1
        tempData=copy.deepcopy(enlarged)

    return enlarged