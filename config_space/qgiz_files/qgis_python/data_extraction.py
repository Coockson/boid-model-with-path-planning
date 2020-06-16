import numpy as np
from osgeo import gdal

# save numpy array as npy file
from numpy import asarray
from numpy import save

dirName = "/home/khaan/Desktop/thesis/config_space/Tif_files/"
dataDirName = "/home/khaan/Desktop/thesis/config_space/data_dir/"
tifName = "30m_config"

ds = gdal.Open(dirName+tifName+".tif")
data_array = np.array(ds.GetRasterBand(1).ReadAsArray())

data_array = data_array.clip(min=0)
data = 1 - data_array

save(dataDirName+tifName+'.npy', data)

