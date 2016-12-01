import numpy as np
import matplotlib.pyplot as plt
import csv
import matplotlib.mlab as mlab
import math
import os.path # for checking file existance

# ----------------- for realsim ----------------
def draw_graph_per_file_realsim(folder_path, scenario, scheme, sim_cnt): #get result from indicated file
  input_file_name = folder_path + "/" + scenario + "/" + scheme + "/" + sim_cnt + "/COOJA.testlog"

  if not os.path.isfile(input_file_name): #if we cannot find file, continue to next loop
    # print "cannot find:", input_file_name, "return"
    return None

  input_file = open(input_file_name)
  input_lines = input_file.readlines()
  input_file.close

  for line in reversed(input_lines):
    if line.find("time expired") > 0: #simulation finished properly
      break
  else:
    # print "cannot find \"time expired\" in", input_file_name, "return"
    return None

  # print "input:", input_file_name

  receive_time_array = []
  receive_packet_id_array = []
  send_time_array = []
  send_packet_id_array = []

  parent_switch_time_array = []

  event_time_array = []
  event_name_array = []

  simulation_start_time=simulation_end_time=0.0

  #------ line looping starts ------
  loop_itr = 0 #ohhhhh stupid
  for line in input_lines: #reversed is important to speed up
    #gathering data to variables
    if "Hello Tada" in line:
      if "Sending" in line:
        time = float(line.split(" ")[4]) / 1000 / 1000 #ms
        send_time_array.append(time)
        packet_id = int(line.split(" ")[12].split("\'")[0])
        send_packet_id_array.append(packet_id)
        last_packet_id = packet_id

      if "received" in line:
        time = float(line.split(" ")[4]) / 1000 / 1000 #s
        receive_time_array.append(time)
        packet_id = int(line.split(" ")[12].split("\'")[0])
        receive_packet_id_array.append(packet_id)

    if "Stable timer expired!!" in line:
      simulation_start_time = float(line.split(" ")[4]) / 1000 / 1000
    elif "Simulation time expired"  in line:
      simulation_end_time = float(line.split(" ")[4]) / 1000 / 1000

    if "rpl_set_preferred_parent" in line:
      time = float(line.split(" ")[4]) / 1000 / 1000
      parent_switch_time_array.append(time)

    if "setedge" in line:
      time = float(input_lines[loop_itr+1].split(" ")[4]) / 1000 / 1000
      event_time_array.append(time)
      event_name_array.append(line.split(" ")[1])

    loop_itr += 1
 
  #----------- drawing starts ---------
  fig, ax = plt.subplots()

  plt.scatter(send_time_array, send_packet_id_array, c='yellow', label="send packet")
  plt.scatter(receive_time_array, receive_packet_id_array, c='blue', label="receive packet")
  plt.scatter(parent_switch_time_array, [0 for i in range(len(parent_switch_time_array))], c='red', label="parent switch")

  #draw event
  plt.scatter(event_time_array, [-2 for i in range(len(event_time_array))], c='green', label="event triggered")
  for x, name in zip(event_time_array, event_name_array):
    plt.axvline(x, c="green")
    plt.text(x, -2, "e:" + name, color="green", ha="left", va='top')

  ax.legend(loc="upper left")
  ax.set_xlim(simulation_start_time, simulation_end_time) #auto fitting based on simulation time
  ax.set_ylim(-5, last_packet_id + 5)
  ax.set_title(scenario + " " + scheme + " " + sim_cnt)  
  ax.set_xlabel("Time (s)")
  ax.set_ylabel("Packet ID")

  fig.savefig(folder_path + "/" + scenario + "/" + "sim-detail_" + scheme + "_" + sim_cnt + ".png")


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# -=-=-=-=-=-= test main =-=-=-=-=-=-
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

if __name__ == "__main__":
  folder_path = "C:/Users/Tada/Documents/Telecom_local/arrange_result_realsim/"
  draw_graph_per_file_realsim(folder_path, "scenario2", "normal-re2", str(39))
  draw_graph_per_file_realsim(folder_path, "scenario2", "leapfrog", str(50))
  draw_graph_per_file_realsim(folder_path, "scenario2", "normal", str(47))
  plt.show()
