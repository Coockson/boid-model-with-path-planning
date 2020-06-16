from numpy import load
import matplotlib.pyplot as plt
import argparse

# load array
data = load('../data_dir/50m_config.npy')

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--map", help="Display configuration space", action="store_true")

args = parser.parse_args()

if(args.map):
    plt.imshow(data, cmap="gray")
    plt.show()

