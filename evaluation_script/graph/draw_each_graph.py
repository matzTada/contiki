#python script file for drawing graph per each results

import numpy as np
import matplotlib.pyplot as plt
import csv
import matplotlib.mlab as mlab
import math

from mod_getdata import get_result_from_file_realsim, get_graph_array_from_data

#data path
datapath = "C:/Users/Tada/Documents/Telecom_local/arrange_result_realsim/scenario2/" #for windows

#parameters for targt files
sim_cnt_min = 31
sim_cnt_max = 50

#---------------------------------------------------------------------------------------------

def draw_line_graph_each(target, element, title, xlabel, ylabel):
  fig, ax = plt.subplots()

  data = target[0]
  xticks = []
  for j in range(0, len(data[0][0])):
    xticks.append(data[0][0][j]["name"])

  for i in range(0, len(data)): #per each simulation
    plot_array = []
    for j in range(0, len(data[i][0])):
      plot_array.append(data[i][0][j][element])
  
    plt.plot(plot_array, label=data[i][1])
    plt.xticks([i for i in range(0, len(xticks))], xticks, rotation=270) #must be changed correpoiding to the number of data

    ax.legend()

  #only for data looks better.
  ax_bar = ax.twinx()
  ax_bar.bar([i for i in range(0, len(xticks))], [0 for i in range(0, len(xticks))], align="center", linewidth=0)
  ax_bar.tick_params(labelright="off")
  
  ax.set_title(title)  
  ax.set_xlabel(xlabel)
  ax.set_ylabel(ylabel)
  fig.savefig(datapath + "sim-line_" + target[1] + "_" + element + ".png")

#---------------------------------------------------------------------------------------------
if __name__ == "__main__":
  print "fight!! ganbare!"

  r_no = get_graph_array_from_data(datapath, "normal", sim_cnt_min, sim_cnt_max)
  r_re2 = get_graph_array_from_data(datapath, "normal-re2", sim_cnt_min, sim_cnt_max)
  r_lf = get_graph_array_from_data(datapath, "leapfrog", sim_cnt_min, sim_cnt_max)

  draw_line_graph_each(r_no, "pdr", r_lf[1], "event", " PDR")
  draw_line_graph_each(r_re2, "pdr", r_re2[1], "event", " PDR")
  draw_line_graph_each(r_lf, "pdr", r_lf[1], "event", " PDR")


  print "---------------------------------------"
  print "--- FIN FIN FIN FIN FIN FIN FIN FIN ---"
  print "---------------------------------------"
  plt.show()
