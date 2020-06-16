import numpy as np
from .config_map_enlarger import enlarge



def save_data(name, output_name, enlarge_factor, scale_factor):
    scaled = enlarge(name,enlarge_factor,scale_factor)
    #grid = 1 - scaled
    np.save('lib/config_space/data_dir/'+ output_name +'.npy',scaled)

def save(name, data):
    np.save('lib/config_space/data_dir/'+ name +'.npy',data)