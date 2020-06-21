import numpy as np
import argparse
from config_space.src.config_map import create_config_space
from config_space.src.config_map_enlarger import enlargecs
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()

parser.add_argument("--src", help="Path to the .npy file", type=str)
parser.add_argument("--form", help="Shape of the swarm starting from (0,0). Ex. \"0,0-10,10-10,0\" ", type=str)
parser.add_argument("--buffer", help="Artificial buffer zone in pixels. E.g 5 ", type=int)
args = parser.parse_args()

init = args.src

mainName = "40m_config"
z = np.load("config_space/data_dir/"+ mainName+".npy")
#cutRange = [1500,2500,1500,2500]
cutRange = [1700,2100,1700,2100]
cutRange = [1700,1750,1700,1750]
config_space = z[cutRange[0]:cutRange[1],cutRange[2]:cutRange[3]]
cs = 1- config_space

form = [[0,0],[0,1],[1,1],[1,0]]
if args.form:
    a = [x.split(",") for x in (str(args.form)).split("-")]
    form = [[int(y) for y in x] for x in a]

artificial = 1
if args.buffer:
    artificial = args.buffer
cs_en = enlargecs(cs,artificial)

cs_fin = create_config_space(form,cs_en,cs.shape)





plt.figure()
plt.title("Original obstacle space")
plt.imshow(cs, cmap='Greys',origin="bottom")

plt.figure()
plt.title("Obstacle space with artificial buffer")
plt.imshow(cs_en, cmap='Greys',origin="bottom")

plt.figure()
plt.title("Configuration space")
plt.imshow(cs_fin, cmap='Greys',origin="bottom")

plt.figure()
form.append([0,0])
xf, yf = zip(*form)
plt.plot(xf,yf,"-")
plt.title("Shape of swarm")
"""plt.xlim(0,cs.shape[0])
plt.ylim(0,cs.shape[1])"""

plt.show()