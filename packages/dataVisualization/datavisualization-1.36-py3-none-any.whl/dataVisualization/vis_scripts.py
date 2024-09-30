'''
A short file for shared functions between visulisation scripts
'''
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

def get_ratio(fig:plt.Figure) -> float:
    size = fig.get_size_inches()*fig.dpi
    print(size)
    w = size[0]
    h = size[1]
    ratio = h/w
    return(ratio)