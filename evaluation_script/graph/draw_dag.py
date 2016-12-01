import numpy as np
import matplotlib.pyplot as plt
import csv
import matplotlib.mlab as mlab
import math
import os.path # for checking file existance

#----------- for OpenCV -------------
import cv2
# from scipy import ndimage

#for graph
from draw_graph_per_simulation import draw_graph_per_file_realsim

NODE_SIZE = 20
FONT = cv2.FONT_HERSHEY_SIMPLEX

class Node:
  def __init__(self, _nodeid, _x, _y):
    self.nodeid = _nodeid
    self.x = _x
    self.y = _y
    self.parentid = 0
    self.altparentid = 0
    self.receive_state = 0
    self.neighbor_array = []

  def refresh(self):
    self.parentid = 0
    self.altparentid = 0
    self.receive_state = 0
    del self.neighbor_array[:]

  def update_parent(self, _parentid):
    self.parentid = _parentid

  def update_altparent(self, _altparentid):
    self.altparentid = _altparentid

  def update_receive_state(self, _state):
    self.receive_state = _state

  def update_neighbor_array(self, _neighborid, _linkquality):
    for tmp_neighbor in self.neighbor_array:
      if tmp_neighbor["neighborid"] == _neighborid: # if already have link information
        tmp_neighbor["linkquality"] = _linkquality
        return
    else:
      self.neighbor_array.append({"neighborid" : _neighborid, "linkquality" : _linkquality})

  def display(self, _img, _node_array, _show_link):
    #parent 
    if self.parentid != 0: #for rpl parent
      for tmp_node in _node_array:
        if self.parentid == tmp_node.nodeid:
          #adjust line length
          x1, y1, x2, y2 = self.x, self.y, tmp_node.x, tmp_node.y
          cos_theta = (x2 - x1) / math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
          sin_theta = (y2 - y1) / math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
          sx = x1 + NODE_SIZE * cos_theta
          sy = y1 + NODE_SIZE * sin_theta
          ex = x2 - NODE_SIZE * cos_theta
          ey = y2 - NODE_SIZE * sin_theta
          cv2.arrowedLine(_img, (int(sx), int(sy)), (int(ex), int(ey)), (0, 0, 255), 5)
    #alt parent
    if self.altparentid != 0: #for rpl parent
      for tmp_node in _node_array:
        if self.altparentid == tmp_node.nodeid:
          #adjust line length
          x1, y1, x2, y2 = self.x, self.y, tmp_node.x, tmp_node.y
          cos_theta = (x2 - x1) / math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
          sin_theta = (y2 - y1) / math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
          sx = x1 + NODE_SIZE * cos_theta
          sy = y1 + NODE_SIZE * sin_theta
          ex = x2 - NODE_SIZE * cos_theta
          ey = y2 - NODE_SIZE * sin_theta
          cv2.arrowedLine(_img, (int(sx), int(sy)), (int(ex), int(ey)), (182, 106, 0), 5)
    #neighbor array
    if len(self.neighbor_array) > 0:
      for tmp_neighbor in self.neighbor_array:
        tmp_neighbor_id = tmp_neighbor["neighborid"]
        tmp_neighbor_linkquality = tmp_neighbor["linkquality"]
        for tmp_node in _node_array:
          if tmp_neighbor_id == tmp_node.nodeid:
            #adjust line length
            x1, y1, x2, y2 = self.x, self.y, tmp_node.x, tmp_node.y
            cos_theta = (x2 - x1) / math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            sin_theta = (y2 - y1) / math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            sx = x1 + NODE_SIZE * cos_theta
            sy = y1 + NODE_SIZE * sin_theta
            ex = x2 - NODE_SIZE * cos_theta
            ey = y2 - NODE_SIZE * sin_theta
            #color based on link
            link_color = (100, 100, 100)
            if tmp_neighbor_linkquality >= 90:
              link_color = (150, 0, 0)
            elif tmp_neighbor_linkquality >= 70:
              link_color = (0, 150, 0)
            elif tmp_neighbor_linkquality >= 50:
              link_color = (0, 150, 150)
            else:
              link_color = (0, 0, 150)
            if _show_link == 1:
              #if tmp_neighbor_linkquality > 90: link_color = (0, 0, 255)
              cv2.line(_img, (int(sx), int(sy)), (int(ex), int(ey)), link_color, 2)
              #text
              cx = (x1 + x2) / 2
              cy = (y1 + y2) / 2
              cv2.putText(_img, str(tmp_neighbor_linkquality), (int(cx), int(cy)), FONT, 0.5, link_color, 2)
    #state 
    state_color = (255, 0, 0) # not receive
    if self.receive_state == 1:
      state_color = (0, 255, 0)
    cv2.circle(_img, (self.x, self.y), NODE_SIZE, state_color, -1)
    cv2.putText(_img, str(self.nodeid), (self.x-NODE_SIZE/2, self.y+NODE_SIZE/2), FONT, 1, (255,255,255), 2)
    # textImg = np.zeros((512,512,3), np.uint8)
    # cv2.putText(textImg, str(self.nodeid), (self.x-NODE_SIZE/2, self.y+NODE_SIZE/2), FONT, 1, (255,255,255), 2)
    # textImg = ndimage.rotate(textImg, -90, reshape=False)
    # img = img+textImg

# ----------------- for realsim ----------------
def extract_event_data_from_file_realsim(folder_path, scenario, scheme, sim_cnt): #get result from indicated file
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

  parent_switch_time_array = []
  parent_switch_array = []

  event_time_array = []
  event_name_array = []

  packet_tracer_array = []
  tmp_packet_tracer = []

  send = 0
  receive = 0

  #------ line looping starts ------
  loop_itr = 0 #ohhhhh stupid
  for line in input_lines: #reversed is important to speed up
    if "Hello" in line:
      if "Sending" in line:
        send += 1
        if send > 1:
          # packet_tracer_array.append(tmp_packet_tracer)
          packet_tracer_array.extend(tmp_packet_tracer)
          tmp_packet_tracer = []
        nodeid = int(line.split(" ")[2])
        time = float(line.split(" ")[4]) / 1000 / 1000 #s
        tmp_packet_tracer.append({"time" : time, "nodeid" : nodeid, "event" : "send"})
      elif "received" in line:
        receive += 1
        nodeid = int(line.split(" ")[2])
        time = float(line.split(" ")[4]) / 1000 / 1000 #s
        tmp_packet_tracer.append({"time" : time, "nodeid" : nodeid, "event" : "receive"})
    elif "LEAPFROG: default route" in line:
      nodeid = int(line.split(" ")[2])
      time = float(line.split(" ")[4]) / 1000 / 1000 #s
      tmp_packet_tracer.append({"time" : time, "nodeid" : nodeid, "event" : "forward"})
    elif "Replication" in line:
      nodeid = int(line.split(" ")[2])
      time = float(line.split(" ")[4]) / 1000 / 1000 #s
      altparentid_str = line.split(" ")[9].strip()
      altparentid = int(altparentid_str)
      tmp_packet_tracer.append({"time" : time, "nodeid" : nodeid, "event" : "replication", "altparentid" : altparentid})
    elif "Simulation time expired" in line:
      # packet_tracer_array.append(tmp_packet_tracer)
      packet_tracer_array.extend(tmp_packet_tracer)

    if "rpl_set_preferred_parent" in line:
      nodeid = int(line.split(" ")[2])
      time = float(line.split(" ")[4]) / 1000 / 1000
      parentid_str = line.split(" ")[7].strip()
      parentid = 0
      if parentid_str != "NULL":
        parentid = int(parentid_str.split(":")[1])
      parent_switch_time_array.append(time)
      parent_switch_array.append({"time" : time, "nodeid" : nodeid, "parentid" : parentid, "event" : "parent_switch"})
      # print "{0:.2f}".format(time), nodeid, "to", parentid

    if "setedge" in line:
      time = float(input_lines[loop_itr+1].split(" ")[4]) / 1000 / 1000 #s
      event_time_array.append(time)
      event_name_array.append(line.split(" ")[1])
      # print line,

    loop_itr += 1

  return parent_switch_array, packet_tracer_array

# ----------------- for realsim ----------------
def extract_linkquality_realsimfuile(folder_path, scenario): #get linkquality from realsimfile
  input_file_name = folder_path + "/" + scenario + "/" + scenario + ".realsimfile"

  if not os.path.isfile(input_file_name): #if we cannot find file, continue to next loop
    # print "cannot find:", input_file_name, "return"
    return None

  input_file = open(input_file_name)
  input_lines = input_file.readlines()
  input_file.close

  # print "input:", input_file_name

  link_event_array = []

  #------ line looping starts ------
  for line in input_lines: #reversed is important to speed up
    if "setedge" in line:
      time = float(line.split(";")[0]) / 1000 #s
      nodeid = int(float(line.split(";")[2]))
      neighborid = int(float(line.split(";")[3]))
      linkquality = int(line.split(";")[4])
      # print time, nodeid, neighborid, linkquality
      link_event_array.append({"time" : time, "nodeid" : nodeid, "event" : "changelink", "neighborid" : neighborid, "linkquality" : linkquality})

  return link_event_array

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# -=-=-=-=-=-= test main =-=-=-=-=-=-
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

if __name__ == "__main__":
  folder_path = "C:/Users/Tada/Documents/Telecom_local/arrange_result_realsim/"
  scenario = "scenario2" #sc4 sc2 sc2 sc2
  scheme = "leapfrog" #leapfrog leapfrog normal normal-re2
  sim_cnt = str(49) #32 50 47 39

  #------------------ for drawing graph -------------------------
  input_file_name = folder_path + "/" + scenario + "/" + scheme + "/" + sim_cnt + "/COOJA.testlog"

  if not os.path.isfile(input_file_name): #if we cannot find file, continue to next loop
    print "cannot find:", input_file_name, "return"
    exit()
  input_file = open(input_file_name)
  input_lines = input_file.readlines()
  input_file.close
  for line in reversed(input_lines):
    if line.find("time expired") > 0: #simulation finished properly
      break
  else:
    print "cannot find \"time expired\" in", input_file_name, "return"
    exit()
  print "input:", input_file_name
  
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
      if len(line.split(" ")) > 3:
        event_name_array.append(line.split(" ")[1] + " " + line.split(" ")[2] + " " + line.split(" ")[3].strip())
      else:
        event_name_array.append(line.split(" ")[1].strip())

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
    plt.text(x, last_packet_id + 5, "e:" + name, color="green", ha="left", va='top', rotation=270)

  ax.legend(loc="upper left")
  # ax.set_xlim(simulation_start_time, simulation_end_time) #auto fitting based on simulation time, auto configuration
  ax.set_xlim(0, simulation_end_time) #auto fitting based on simulation time
  ax.set_ylim(-5, last_packet_id + 5)
  ax.set_title(scenario + " " + scheme + " " + sim_cnt)  
  ax.set_xlabel("Time (s)")
  ax.set_ylabel("Packet ID")

  #this is for the vertical line
  event_time_vertical_line = plt.axvline(0)

  #------------------ end drawing graph -------------------------

  #------------------------------------------for drawing dag
  parent_switch_array, packet_tracer_array = extract_event_data_from_file_realsim(folder_path, scenario, scheme, sim_cnt)
  mixed_list = []
  mixed_list.extend(parent_switch_array)
  mixed_list.extend(packet_tracer_array)
  mixed_list.sort(key=lambda x:x["time"])
  # print mixed_list
  # 
  link_event_array = extract_linkquality_realsimfuile(folder_path, scenario)
  mixed_list.extend(link_event_array)
  mixed_list.sort(key=lambda x:x["time"])

  # Create a black image, a window and bind the function to window
  img = np.zeros((512,512,3), np.uint8)
  window_name = scenario + " " + scheme + " " + sim_cnt
  cv2.namedWindow(window_name)

  n1 = Node(1, 255, 38)
  n2 = Node(2, 189, 129)
  n3 = Node(3, 321, 130)
  n4 = Node(4, 193, 249)
  n5 = Node(5, 325, 250)
  n6 = Node(6, 194, 367)
  n7 = Node(7, 327, 367)
  n8 = Node(8, 262, 464)

  node_array = [n1, n2, n3, n4, n5, n6, n7, n8]
  
  cnt_event = 0
  current_event_time = 0

  show_link_flag = 1 # for displaying link

  while(1): #drawing loop, I think I can say draw() in Procesing
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
      break
    elif k == ord('s'):
      print "pressed:", chr(k)
      e_time = parent_switch_array[cnt_event]["time"]
      e_nodeid = parent_switch_array[cnt_event]["nodeid"]
      e_parentid = parent_switch_array[cnt_event]["parentid"]
      print "event:", e_time, e_nodeid, e_parentid
      for tmp_node in node_array:
        if tmp_node.nodeid == e_nodeid:
          tmp_node.update_parent(e_parentid)
      cnt_event += 1
      if cnt_event >= len(parent_switch_array):
        break
    elif k == ord('l'): #link quality
      print "pressed:", chr(k)
      e_time = link_event_array[cnt_event]["time"]
      e_nodeid = link_event_array[cnt_event]["nodeid"]
      e_neighborid = link_event_array[cnt_event]["neighborid"]
      e_linkquality = link_event_array[cnt_event]["linkquality"]
      print "event:", e_time, e_nodeid, e_neighborid, e_linkquality
      for tmp_node in node_array:
        if tmp_node.nodeid == e_nodeid:
          tmp_node.update_neighbor_array(e_neighborid, e_linkquality)
      cnt_event += 1
      if cnt_event >= len(link_event_array):
        break
    elif k == ord('L'):
      show_link_flag = 1 - show_link_flag
    elif k == ord('e'): #move forward events
      # print "pressed:", chr(k)
      print "cnt_event", cnt_event,
      e_event = mixed_list[cnt_event]["event"]
      e_time = mixed_list[cnt_event]["time"]
      e_nodeid = mixed_list[cnt_event]["nodeid"]
      print "{0:.2f}".format(e_time), e_nodeid, e_event,
      current_event_time = e_time
      #change node parameters based on events
      if e_event == "parent_switch":
        e_parentid = mixed_list[cnt_event]["parentid"]
        print e_parentid,
        for tmp_node in node_array:
          if tmp_node.nodeid == e_nodeid:
            tmp_node.update_parent(e_parentid)
      elif e_event == "send":# initialize
        for tmp_node in node_array:
          tmp_node.update_receive_state(0) 
      elif e_event == "forward":
        for tmp_node in node_array:
          if tmp_node.nodeid == e_nodeid:
            tmp_node.update_receive_state(1)
      elif e_event == "receive":
        for tmp_node in node_array:
          if tmp_node.nodeid == e_nodeid:
            tmp_node.update_receive_state(1)
      elif e_event == "replication":
        e_altparentid = mixed_list[cnt_event]["altparentid"]
        print e_altparentid,
        for tmp_node in node_array:
          if tmp_node.nodeid == e_nodeid:
            tmp_node.update_altparent(e_altparentid)
      elif e_event == "changelink":      
        e_neighborid = mixed_list[cnt_event]["neighborid"]
        e_linkquality = mixed_list[cnt_event]["linkquality"]
        print e_neighborid, e_linkquality,
        for tmp_node in node_array:
          if tmp_node.nodeid == e_nodeid:
            tmp_node.update_neighbor_array(e_neighborid, e_linkquality)            
      print

      #update graph of matplotlib
      event_time_vertical_line.set_xdata(current_event_time)
      fig.canvas.draw()

      #increase event counter
      cnt_event += 1
      if cnt_event >= len(mixed_list):
        break #finish visualizer
    elif k == ord('b'): #move back. crazy
      if cnt_event < 1:
        print "cannot move back"
      else:
        cnt_event -= 1
        for tmp_node in node_array:
          tmp_node.refresh()
        e_event = ""
        e_time = 0
        e_nodeid = 0
        current_event_time = e_time
        for i in range(0, cnt_event):
          e_event = mixed_list[i]["event"]
          e_time = mixed_list[i]["time"]
          e_nodeid = mixed_list[i]["nodeid"]
          current_event_time = e_time

          if e_event == "parent_switch":
            e_parentid = mixed_list[i]["parentid"]
            for tmp_node in node_array:
              if tmp_node.nodeid == e_nodeid:
                tmp_node.update_parent(e_parentid)
          elif e_event == "send":# initialize
            for tmp_node in node_array:
              tmp_node.update_receive_state(0) 
          elif e_event == "forward":
            for tmp_node in node_array:
              if tmp_node.nodeid == e_nodeid:
                tmp_node.update_receive_state(1)
          elif e_event == "receive":
            for tmp_node in node_array:
              if tmp_node.nodeid == e_nodeid:
                tmp_node.update_receive_state(1)
          elif e_event == "replication":
            e_altparentid = mixed_list[i]["altparentid"]
            for tmp_node in node_array:
              if tmp_node.nodeid == e_nodeid:
                tmp_node.update_altparent(e_altparentid)
          elif e_event == "changelink":      
            e_neighborid = mixed_list[i]["neighborid"]
            e_linkquality = mixed_list[i]["linkquality"]
            for tmp_node in node_array:
              if tmp_node.nodeid == e_nodeid:
                tmp_node.update_neighbor_array(e_neighborid, e_linkquality)            

        print "cnt_event", cnt_event-1, "{0:.2f}".format(e_time), e_nodeid, e_event
        event_time_vertical_line.set_xdata(current_event_time)
        fig.canvas.draw()
        
    #--------- for drawing. This functions called every loop --------
    img = np.zeros((512,512,3), np.uint8) #initialize img
    for tmp_node in node_array:
      tmp_node.display(img, node_array, show_link_flag)

    cv2.putText(img, window_name, (0, 20), FONT, 0.5, (255,255,255), 1)
    if cnt_event < 2: #first
      cv2.putText(img, "First", (0, 40), FONT, 0.5, (255,255,255), 1)
    else:
      cv2.putText(img, "Before " + "{0:.2f}".format(mixed_list[cnt_event-2]["time"]) + "  " + str(mixed_list[cnt_event-2]["nodeid"]) + " " + str(mixed_list[cnt_event-2]["event"]), (0, 40), FONT, 0.5, (255,255,255), 1)
    cv2.putText(img, "Current " + "{0:.2f}".format(current_event_time) + "  " + str(mixed_list[cnt_event]["nodeid"]) + " " + str(mixed_list[cnt_event]["event"]), (0, 60), FONT, 0.5, (255,255,255), 1)
    if cnt_event >= len(mixed_list) - 1:
      cv2.putText(img, "Last", (0, 80), FONT, 0.5, (255,255,255), 1)
    else:
      cv2.putText(img, "Next " + "{0:.2f}".format(mixed_list[cnt_event+1]["time"]) + "  " + str(mixed_list[cnt_event+1]["nodeid"]) + " " + str(mixed_list[cnt_event+1]["event"]), (0, 80), FONT, 0.5, (255,255,255), 1)
    cv2.imshow(window_name,img)
    #------------ drawing graphs
    plt.pause(.01)    #do not use fig.show() http://qiita.com/hausen6/items/b1b54f7325745ae43e47

  cv2.destroyAllWindows()