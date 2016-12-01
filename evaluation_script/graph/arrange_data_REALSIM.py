#python script file for extracting data from Cooja simulation result
#NOT needed now (9/Sep/2016) put this file in the same directory where "leapfrog" "normal" etc... exist
#This script is for the result with RealSim over DGRM. get_result_from_file_realsim must be used to readfiles

import numpy as np
import matplotlib.pyplot as plt
import csv
import matplotlib.mlab as mlab
import math


from mod_getdata import get_result_from_file_realsim, get_graph_array_from_data, set_boxplot_color

#data path
datapath = "C:/Users/Tada/Documents/Telecom_local/arrange_result_realsim/scenario4/" #for windows

#parameters for targt files
sim_cnt_min = 1
sim_cnt_max = 100

graph_label_dict = {"normal" : "RT0", "normal-re2" : "RT2", "normal-re4" : "RT4", "normal-re6" : "RT6", "normal-re8" : "RT8", "leapfrog" : "LC"}
graph_color_dict = {"normal" : "orange", "normal-re2" : "red", "normal-re4" : "magenta", "normal-re6" : "blue", "normal-re8" : "cyan", "leapfrog" : "green"}
graph_format_dict = {"normal" : "x", "normal-re2" : "s", "normal-re4" : "v", "normal-re6" : "p", "normal-re8" : "d", "leapfrog" : "o"}
graph_hatch_dict = {"normal" : "/", "normal-re2" : "*", "normal-re4" : "o", "normal-re6" : "O", "normal-re8" : ".", "leapfrog" : "\\"}

def draw_line_graph_combined(target_scheme, element, xlabel, ylabel, number_col, legend_position, lp_x, lp_y, adjust_flag, adjust_left, adjust_bottom, adjust_right, adjust_top, connected_flag):
  fig, ax = plt.subplots()

  print "------- " + ylabel + " average of all simulation -------"

  for target in target_scheme:
    data = target[0]
    xticks = ["def", "\nid:2", "def", "\nid:5", "def", "\nid:6", "def", "\nid:3", "def", "\nid:4", "def", "\nid:7", "def"] #dirty mode
    # xticks = [] #use this for general
    # for j in range(0, len(data[0][0])):
    #   xticks.append(data[0][0][j]["name"])
    plot_array = []
    plot_error = []
    for j in range(0, len(data[0][0])):
      tmp_avg_calc_array = []
      for i in range(0, len(data)):
        data_element = data[i][0][j][element]
        if element == "pdr" and data_element >=1:
          data_element = 1
        tmp_avg_calc_array.append(data_element)
      plot_array.append(np.average(tmp_avg_calc_array))
      plot_error.append(np.std(tmp_avg_calc_array))

    print element + " " + target[1] + " " + str(np.average(plot_array)) # for detailed data

    # plt.plot(plot_array, label=graph_label_dict[counter])
    # plt.xticks([i for i in range(0, len(xticks))], xticks, rotation=0) #must be changed correpoiding to the number of data

    if connected_flag == 1:
      ax.errorbar([i for i in range(0, len(xticks))], plot_array, yerr=plot_error, label=graph_label_dict[target[1]], color=graph_color_dict[target[1]])
    else:
      ax.errorbar([i for i in range(0, len(xticks))], plot_array, yerr=plot_error, label=graph_label_dict[target[1]], color=graph_color_dict[target[1]], fmt=graph_format_dict[target[1]])

    plt.xticks([i for i in range(0, len(xticks))], xticks, rotation=0) #must be changed correpoiding to the number of data
    plt.rcParams['font.size'] = 15
    ax.legend(ncol=number_col, loc=legend_position, bbox_to_anchor=(lp_x, lp_y))
    if(adjust_flag == 1):
      plt.subplots_adjust(left=adjust_left, bottom=adjust_bottom, right=adjust_right, top=adjust_top)

    #only for data looks better.
    ax_bar = ax.twinx()
    ax_bar.bar([i for i in range(0, len(xticks))], [0 for i in range(0, len(xticks))], align="center", linewidth=0, color='w')
    ax_bar.tick_params(labelright="off")
  
  ax.set_xlabel(xlabel, fontsize=20)
  ax.set_ylabel(ylabel, fontsize=20)

  if connected_flag == 1:
    fig.savefig(datapath + "line/" + element + ".png")
    fig.savefig(datapath + "line/" + element + ".eps")
  else:
    fig.savefig(datapath + "line_not_connected/" + element + ".png")
    fig.savefig(datapath + "line_not_connected/" + element + ".eps")

#added 2016/10/24
def draw_box_graph_combined(target_scheme, element, xlabel, ylabel, number_col, legend_position, lp_x, lp_y, adjust_flag, adjust_left, adjust_bottom, adjust_right, adjust_top, separated_flag):
  fig, ax = plt.subplots()

  separate_itr = 0
  for target in target_scheme: #this scheme should be "normal", "normal-re2,4,6,8", "leapfrog"
    data = target[0]
    plot_array = []
    for j in range(0, len(data[0][0])):
      tmp_array = [] #tmp_array has data of 1 specified event in 1 specified scheme
      for i in range(0, len(data)):
        data_element = data[i][0][j][element]
        if element == "pdr" and data_element >=1:
          data_element = 1
        tmp_array.append(data_element)
      plot_array.append(tmp_array)

    for i in range(0, len(plot_array)):
      if separated_flag == 1:
        bp = plt.boxplot(plot_array[i], positions=[i * (len(target_scheme) + 1) + separate_itr], patch_artist=True, widths=0.5) #separated 
      else:
        bp = plt.boxplot(plot_array[i], positions=[i], patch_artist=True, widths=0.7) #not separated 
      set_boxplot_color(bp, graph_color_dict[target[1]], graph_hatch_dict[target[1]]) 

    separate_itr += 1

  xticks = ["def", "\nid:2", "def", "\nid:5", "def", "\nid:6", "def", "\nid:3", "def", "\nid:4", "def", "\nid:7", "def"] #dirty mode
  # xticks = [] #use this for general
  # for j in range(0, len(data[0][0])):
  #   xticks.append(data[0][0][j]["name"])
  if separated_flag == 1:
    xticks_refined = []
    original_xticks_itr = 0
    for i in range(0, len(data[0][0]) * (len(target_scheme) + 1)):
      if (i % (len(target_scheme) + 1)) == int((len(target_scheme) + 1)/ 2):
        xticks_refined.append(xticks[original_xticks_itr])
        original_xticks_itr += 1
      else:
        xticks_refined.append("")
    plt.xticks([i for i in range(0, len(xticks_refined))], xticks_refined, rotation=0)
  else:
    plt.xticks([i for i in range(0, len(xticks))], xticks, rotation=0) #must be changed correpoiding to the number of data

  plt.rcParams['font.size'] = 15

  #only used for making legends
  for target in target_scheme: #this scheme should be "normal", "normal-re2,4,6,8", "leapfrog"
    ax.bar([1], [0], color='white', edgecolor=graph_color_dict[target[1]], hatch=graph_hatch_dict[target[1]], label=graph_label_dict[target[1]])
  ax.legend(ncol=number_col, loc=legend_position, bbox_to_anchor=(lp_x, lp_y))
  if(adjust_flag == 1):
    plt.subplots_adjust(left=adjust_left, bottom=adjust_bottom, right=adjust_right, top=adjust_top)

  #only for data looks better.
  ax_bar = ax.twinx()
  ax_bar.bar([i for i in range(0, len(xticks))], [0 for i in range(0, len(xticks))], align="center", linewidth=0, color='w')
  ax_bar.tick_params(labelright="off")
  
  ax.set_xlabel(xlabel, fontsize=20)
  ax.set_ylabel(ylabel, fontsize=20)

  if separated_flag == 1:
    fig.savefig(datapath + "box_sep/" + element + ".png")
    fig.savefig(datapath + "box_sep/" + element + ".eps")
  else:
    fig.savefig(datapath + "box/" + element + ".png")
    fig.savefig(datapath + "box/" + element + ".eps")

def gaussian_distribution_data_analyze(target, element, reject_sigma):
  data = target[0]
  remove_set = set([])
  print "gd_analyze", target[1], element, "#data", len(data) 
  for j in range(0, len(data[0][0])): #check for each events
    tmp_array = []
    for i in range(0, len(data)):
      tmp_array.append(data[i][0][j][element])
    tmp_ave = np.average(tmp_array)
    tmp_std = np.std(tmp_array)

    count1=count2=count3=count_r=0
    for i in range(0, len(tmp_array)):
      if abs(tmp_array[i] - tmp_ave) >= 3 * tmp_std:
        count3 += 1 
      if abs(tmp_array[i] - tmp_ave) >= 2 * tmp_std:
        count2 += 1 
      if abs(tmp_array[i] - tmp_ave) >= 1 * tmp_std:
        count1 += 1 
      if abs(tmp_array[i] - tmp_ave) >= reject_sigma * tmp_std:
        count_r += 1
        remove_set.add(i)
        # print "i", i, "{0:.2f}".format(tmp_array[i])
    # print "linkquality", data[0][j]["name"], "ave", "{0:.2f}".format(tmp_ave), "std", "{0:.2f}".format(tmp_std),
    # print "sigma_r", "{0:.0f}".format(count_r), "sigma3", "{0:.0f}".format(count3), "sigma2", "{0:.0f}".format(count2), "sigma1", "{0:.0f}".format(count1)
  if len(remove_set) == 0: #nothing to remove
    print "gd_analyzed nothing to remove with sigma", reject_sigma, "Return original"
    return target
  elif len(remove_set) == len(data): #please do not remove all ;-(
    print "gd_analyzed all will be rejected with sigma", reject_sigma, "Return original"
    return target
  else: #remove process
    print "gd_analyzed reject", sorted(remove_set), "with reject_sigma", reject_sigma, 
    pop_slide = 0
    for r_s_value in sorted(remove_set):
      i = r_s_value - pop_slide #this is important to remoce data from array. When pop one, the sequenence number will be changed
      # print "i", i,
      # for j in range(0, len(data[i])):
      #   print data[i][j][element],
      # print
      data.pop(i)
      pop_slide += 1
    print "#data", len(data)
    return data, target[1]

#-------------------------- main start -------------------------------

#--------------arrange data -------------------
print "---------------------------------------"
print "----try to arrange data from Normal----"
print "---------------------------------------"

r_no = get_graph_array_from_data(datapath, "normal", sim_cnt_min, sim_cnt_max)

print "---------------------------------------"
print "-try to arrange data from Normal ReTx-2-"
print "---------------------------------------"

r_re2 = get_graph_array_from_data(datapath, "normal-re2", sim_cnt_min, sim_cnt_max)

print "---------------------------------------"
print "-try to arrange data from Normal ReTx-4-"
print "---------------------------------------"

r_re4 = get_graph_array_from_data(datapath, "normal-re4", sim_cnt_min, sim_cnt_max)

print "---------------------------------------"
print "-try to arrange data from Normal ReTx-6-"
print "---------------------------------------"

r_re6 = get_graph_array_from_data(datapath, "normal-re6", sim_cnt_min, sim_cnt_max)

print "---------------------------------------"
print "-try to arrange data from Normal ReTx-8-"
print "---------------------------------------"

r_re8 = get_graph_array_from_data(datapath, "normal-re8", sim_cnt_min, sim_cnt_max)

print "---------------------------------------"
print "---try to arrange data from Leapfrog---"
print "---------------------------------------"

r_lf = get_graph_array_from_data(datapath, "leapfrog", sim_cnt_min, sim_cnt_max)


#Removing outliner automatically by Gaussian Distribution with Maha thanks! like you!
print "---------------------------------------"
print "--Gaussian Distribution Data Analyze---"
print "---------------------------------------"
for target in [r_no, r_re2, r_re4, r_re6, r_re8, r_lf]:
  target = gaussian_distribution_data_analyze(target, "pdr", 2)

# # line graph
# #--------------PDR boxplot-------------
# draw_line_graph_combined([r_no, r_re2, r_re4, r_re6, r_re8, r_lf], "pdr", "Events", "PDR (%)", 1, "upper left", 1, 1, 1, 0.15, 0.15, 0.8, 0.9, 1)
# #--------------delay boxplot-------------
# draw_line_graph_combined([r_no, r_re2, r_re4, r_re6, r_re8, r_lf], "delay", "Events", "Delay (ms)", 2, "upper left", 0, 1, 1, 0.15, 0.15, 0.9, 0.9, 1)
# #--------------jitter boxplot-------------
# draw_line_graph_combined([r_no, r_re2, r_re4, r_re6, r_re8, r_lf], "jitter", "Events", "Jitter (ms)", 1, "upper left", 1, 1, 1, 0.15, 0.15, 0.8, 0.9, 1)
# #--------------Duty Cycle-------------
# draw_line_graph_combined([r_no, r_re2, r_re4, r_re6, r_re8, r_lf], "dutycycle", "Events", "Duty Cycle (%)", 2, "upper right", 1, 1, 1, 0.15, 0.15, 0.9, 0.9, 1)
# #--------------efficiency boxplot-------------
# draw_line_graph_combined([r_no, r_re2, r_re4, r_re6, r_re8, r_lf], "efficiency", "Events", "Efficienty=pdr/delay_avg(%/s)", 1, "upper right", 1, 1, 1, 0.15, 0.15, 0.9, 0.9, 1)
# #--------------Energy boxplot-------------
# draw_line_graph_combined([r_no, r_re2, r_re4, r_re6, r_re8, r_lf], "energy", "Events", "Average energy consumption of nodes (mW)", 1, "upper right", 1, 1, 1, 0.15, 0.15, 0.9, 0.9, 1)

# line graph not connected
#--------------PDR boxplot-------------
draw_line_graph_combined([r_no, r_re2, r_re4, r_re6, r_re8, r_lf], "pdr", "Events", "PDR (%)", 1, "upper left", 1, 1, 1, 0.15, 0.15, 0.8, 0.9, 0)
#--------------delay boxplot-------------
draw_line_graph_combined([r_no, r_re2, r_re4, r_re6, r_re8, r_lf], "delay", "Events", "Delay (ms)", 2, "upper left", 0, 1, 1, 0.15, 0.15, 0.9, 0.9, 0)
#--------------jitter boxplot-------------
draw_line_graph_combined([r_no, r_re2, r_re4, r_re6, r_re8, r_lf], "jitter", "Events", "Jitter (ms)", 1, "upper left", 1, 1, 1, 0.15, 0.15, 0.8, 0.9, 0)
#--------------Duty Cycle-------------
draw_line_graph_combined([r_no, r_re2, r_re4, r_re6, r_re8, r_lf], "dutycycle", "Events", "Duty Cycle (%)", 2, "upper right", 1, 1, 1, 0.15, 0.15, 0.9, 0.9, 0)
#--------------efficiency boxplot-------------
draw_line_graph_combined([r_no, r_re2, r_re4, r_re6, r_re8, r_lf], "efficiency", "Events", "Efficienty=pdr/delay_avg(%/s)", 1, "upper right", 1, 1, 1, 0.15, 0.15, 0.9, 0.9, 0)
#--------------Energy boxplot-------------
draw_line_graph_combined([r_no, r_re2, r_re4, r_re6, r_re8, r_lf], "energy", "Events", "Average energy consumption of nodes (mW)", 1, "upper right", 1, 1, 1, 0.15, 0.15, 0.9, 0.9, 0)

# # box graph
# #--------------PDR boxplot-------------
# draw_box_graph_combined([r_no, r_re2, r_re4, r_re6, r_re8, r_lf], "pdr", "Events", "PDR (%)", 1, "upper left", 1, 1, 1, 0.15, 0.15, 0.8, 0.9, 0)
# #--------------delay boxplot-------------
# draw_box_graph_combined([r_no, r_re2, r_re4, r_re6, r_re8, r_lf], "delay", "Events", "Delay (ms)", 1, "upper left", 1, 1, 1, 0.15, 0.15, 0.8, 0.9, 0)
# #--------------jitter boxplot-------------
# draw_box_graph_combined([r_no, r_re2, r_re4, r_re6, r_re8, r_lf], "jitter", "Events", "Jitter (ms)", 1, "upper left", 1, 1, 1, 0.15, 0.15, 0.8, 0.9, 0)
# #--------------Duty Cycle-------------
# draw_box_graph_combined([r_no, r_re2, r_re4, r_re6, r_re8, r_lf], "dutycycle", "Events", "Duty Cycle (%)", 1, "upper left", 1, 1, 1, 0.15, 0.15, 0.8, 0.9, 0)
# #--------------efficiency boxplot-------------
# draw_box_graph_combined([r_no, r_re2, r_re4, r_re6, r_re8, r_lf], "efficiency", "Events", "Efficienty=pdr/delay_avg(%/s)", 1, "upper left", 1, 1, 1, 0.15, 0.15, 0.8, 0.9, 0)
# #--------------Energy boxplot-------------
# draw_box_graph_combined([r_no, r_re2, r_re4, r_re6, r_re8, r_lf], "energy", "Events", "Average energy consumption of nodes (mW)", 1, "upper left", 1, 1, 1, 0.15, 0.15, 0.8, 0.9, 0)

# # box graph separated
# #--------------PDR boxplot-------------
# draw_box_graph_combined([r_no, r_re2, r_re4, r_re6, r_re8, r_lf], "pdr", "Events", "PDR (%)", 1, "upper left", 1, 1, 1, 0.15, 0.15, 0.8, 0.9, 1)
# #--------------delay boxplot-------------
# draw_box_graph_combined([r_no, r_re2, r_re4, r_re6, r_re8, r_lf], "delay", "Events", "Delay (ms)", 1, "upper left", 1, 1, 1, 0.15, 0.15, 0.8, 0.9, 1)
# #--------------jitter boxplot-------------
# draw_box_graph_combined([r_no, r_re2, r_re4, r_re6, r_re8, r_lf], "jitter", "Events", "Jitter (ms)", 1, "upper left", 1, 1, 1, 0.15, 0.15, 0.8, 0.9, 1)
# #--------------Duty Cycle-------------
# draw_box_graph_combined([r_no, r_re2, r_re4, r_re6, r_re8, r_lf], "dutycycle", "Events", "Duty Cycle (%)", 1, "upper left", 1, 1, 1, 0.15, 0.15, 0.8, 0.9, 1)
# #--------------efficiency boxplot-------------
# draw_box_graph_combined([r_no, r_re2, r_re4, r_re6, r_re8, r_lf], "efficiency", "Events", "Efficienty=pdr/delay_avg(%/s)", 1, "upper left", 1, 1, 1, 0.15, 0.15, 0.8, 0.9, 1)
# #--------------Energy boxplot-------------
# draw_box_graph_combined([r_no, r_re2, r_re4, r_re6, r_re8, r_lf], "energy", "Events", "Average energy consumption of nodes (mW)", 1, "upper left", 1, 1, 1, 0.15, 0.15, 0.8, 0.9, 1)


# ---------------fin and show -------------
print "------------------------------------------------------------------------------"
print "finish to draw figures. Plase look at ", datapath
print "finish to draw figures. Plase look at ", datapath
print "finish to draw figures. Plase look at ", datapath
print "------------------------------------------------------------------------------"
plt.show()