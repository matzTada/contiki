#python module for evaluation. 

import numpy as np
import os.path # for checking file existance

# Z1 zolertia sensor average power total energy consumption calculation.
# Logfile from Contiki os powertrace.
#Declaring the currents as they are in Zoletrias Z1 datasheet.
CURRENTS = {
    "voltage" : 3,
    "power_lpm_mA" : 0.05,
    "power_cpu_mA" : 1.8,
    "power_tx_mA"  : 17.4,
    "power_rx_mA"  : 18.8,
    "power_idle_mA": 0.416,
}

NUM_NODES = 8 #the number of node in network

# -------------------functions------------------
# ------------- CAUTION!! jitter is not modified!!!!! ------------------
# ------------- CAUTION!! jitter is not modified!!!!! ------------------
# ------------- CAUTION!! jitter is not modified!!!!! ------------------
def get_result_from_file(input_file_name): #get result from indicated file
	input_file = open(input_file_name)
	input_lines = input_file.readlines()
	input_file.close

	#for time
	time_counted_start = 0.0
	time_counted_end = 0.0

	#for counting 
	pdr = 0.0
	send = 0.0
	receive = 0.0
	replication = 0.0
	elimination = 0.0
	first_hello_flag = 0
	replication_cnt_array = []

	#for delay
	#in successful transmission delay is caluclated as the difference between the time when sender sends data and the time receiver receives the data
	delay_time_send_array = np.zeros(1000)
	delay_time_receive_array = np.zeros(1000)
	delay_time_array = []

	#for jitter
	jitter_last_time = 0.0
	jitter_time_array = []

	#initialize array
	for i in range(0, NUM_NODES):
		replication_cnt_array.append(0.0)

	#Declaring other vars and arrays
	TICKS_PER_SECOND = 32768
	EnergyTable      = []  # Energy:cpu,lpm,rx,tx,idle
	TmpTable         = []
	AVG=TOT=Cpu=Lpm=Tx=Rx=TOTtx=AVGtx=TOTtx=TOTrx=0.0
	tmp              = []

	for line in input_lines: #reversed is important to speed up
		#for time
		if "Stable timer expired!!" in line:
			tmp_split_line = line.split(" ")
			time_counted_start = int(tmp_split_line[4])
		elif "Simulation time expired" in line:
			tmp_split_line = line.split(" ")
			time_counted_end = int(tmp_split_line[4])

        	#for calculating energy
		if "PWR" in line:       #Cooja powertrace output "PowerF" in this example generaly is "P"
			tmp1 = line.split(" ")
			tmp1 = filter(None,tmp1)
			Cpu=Cpu+int(tmp1[15])             
			Lpm=Lpm+int(tmp1[16])
			Tx=Tx+int(tmp1[17])
			Rx=Rx+int(tmp1[18])
		
		if "Hello Tada" in line:
			if ("Hello TadaMatz 1" in line) or ("Hello Tada 0001" in line):
				first_hello_flag = 1
			if not (("Hello TadaMatz 0" in line) or ("Hello Tada 0000" in line)):
				if "Sending" in line:
					send += 1
					#for delay
					tmp_split_line = line.split(" ")
					delay_time_send = float(tmp_split_line[4]) / 1000 #ms
					tmp_str = tmp_split_line[12].split("\'") #for old version send
					# tmp_str = tmp_split_line[12].split("\'") #for new version
					tmp_packet_id = int(tmp_str[0])
					delay_time_send_array[tmp_packet_id] = delay_time_send
				elif "received" in line:
					receive += 1
					#for delay
					tmp_split_line = line.split(" ")
					delay_time_receive = float(tmp_split_line[4]) / 1000 #ms
					tmp_str = tmp_split_line[20].split("\'") #for old version receive
					# tmp_str = tmp_split_line[12].split("\'") #for new version
					tmp_packet_id = int(tmp_str[0])
					delay_time_array.append(delay_time_receive - delay_time_send_array[tmp_packet_id])
					if receive == 0: #first packet
						jitter_last_time = delay_time_receive
					else:
						jitter_time_array.append(delay_time_receive - jitter_last_time) #time of current packet received - time of last packet received
						jitter_last_time = delay_time_receive

		if ("Replication" in line) and (first_hello_flag == 1):
			tmp_split_line = line.split(" ")
			temp_sid = int(tmp_split_line[2]) - 1
			replication_cnt_array[temp_sid] += 1
			replication += 1
		elif ("Elimination" in line) and (first_hello_flag == 1):
			elimination += 1
	
	#for time
	counted_time_length_sec = (time_counted_end - time_counted_start) / 1000 / 1000
	
	#for communication
	if send > 0:
		pdr = receive / send
	else:
		pdr = 0
	
	#for energy
	TmpTable.insert(0, Cpu)
	TmpTable.insert(1, Lpm)
	TmpTable.insert(2, Tx)
	TmpTable.insert(3, Rx)

	for i in range(0,4):
		EnergyTable.append(float(TmpTable[i])/TICKS_PER_SECOND) #From ticks to seconds conversion                                                       

	#Calculating the Energy of each state(Cpu,lpm,tx,rx,idle=0)
	EnergyTable[0] = EnergyTable[0]* CURRENTS["power_cpu_mA"]*CURRENTS["voltage"]
	EnergyTable[1] = EnergyTable[1]* CURRENTS["power_lpm_mA"]*CURRENTS["voltage"]
	EnergyTable[2] = EnergyTable[2]* CURRENTS["power_tx_mA"] *CURRENTS["voltage"]
	EnergyTable[3] = EnergyTable[3]* CURRENTS["power_rx_mA"] *CURRENTS["voltage"]

	for i in range(0,4): #Adding them all together
	    AVG = EnergyTable[i] + AVG
	    TOT = EnergyTable[i] + TOT

	AVG = AVG/counted_time_length_sec #Calculating average power for n minutes of simulation here for 1 hour simulation(60-minutes)

	#for delay
	delay_avg = 0.0
	if len(delay_time_array) > 0:
		delay_avg = np.average(delay_time_array)

	#for jitter
	jitter_avg = 0.0
	if len(jitter_time_array) > 0:
		jitter_avg = np.average(jitter_time_array)

	#for efficiency
	efficiency = 0
	if delay_avg > 0:
		efficiency = pdr/delay_avg * 1000 #(%/s)

	#print
	# print "input:", input_file_name,
	# print "pdr:", "{0:.2f}".format(pdr), "s:", send, "r:", receive, "delay(ms):", "{0:.2f}".format(delay_avg), "jitter(ms):", "{0:.2f}".format(jitter_avg),
	# print "efficiency(%/s):", "{0:.5f}".format(efficiency)
	# print "replication:", replication, "elimination:", elimination
	# print "TOT_NET(mj):", TOT, "AVG_NET(mW):", AVG, "TOT_NODE(mj):", TOT/NUM_NODES, "AVG_NODE(mW):", AVG/NUM_NODES
	# print "counted_time_length_sec", counted_time_length_sec
	# print "replication_cnt_array: ",	
	# for i in range(0, NUM_NODES):
	# 	print str(i+1) + ":", str(replication_cnt_array[i]),
	# print ""
	# print "total replication:", str(sum(replication_cnt_array))

	#return
	return (pdr, send, receive, replication, elimination, \
		TOT, AVG, TOT/NUM_NODES, AVG/NUM_NODES, \
		delay_avg, jitter_avg, efficiency)

def get_randomseed_from_file(input_file_name): #get data from input file
	input_file = open(input_file_name)
	input_lines = input_file.readlines()
	input_file.close

	for line in input_lines: #reversed is important to speed up
		#for time
		if "random" in line:
			randomseed = int(line.split(":")[4])
			return randomseed
	else:
		return ""

def set_boxplot_color(bp, color_name, hatch_name):
	bp['boxes'][0].set(edgecolor=color_name, hatch=hatch_name)
	bp['medians'][0].set(color=color_name)
	bp['caps'][0].set(color=color_name) #width of upper line
	bp['caps'][1].set(color=color_name) #width of lower line
	bp['whiskers'][0].set(color=color_name) #width to upper line
	bp['whiskers'][1].set(color=color_name) #width to lower line


# ----------------- for realsim ----------------
# ------------- jitter is modified!!!!! ------------------
def get_result_from_file_realsim(input_file_name): #get result from indicated file
# return data in following array structure from 1 simulation file
#  [event1,event2,event3,...]
#    event = dict of {"event_id", "name", "pdr", "rep", "eli", "delay", "jitter", "energy", "efficiency",...}
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

	#---------- return valuables ----------
	r_event_id = 0
	r_array = []


	#yeah, input_file worths to calculate
	#----------initiazlize variables----------
	#for time
	time_counted_start=time_counted_end=counted_time_length_sec=0.0
	INTERVAL_LINK_CHANGE = 300 #if INTERVAL_LINK_CHANGE > 0, time for Energy calculation is fixed
	
	#for counting 
	pdr=send=receive=replication=elimination=0.0
	# replication_cnt_array = []
	# for i in range(0, NUM_NODES): 	#initialize array
	# 	replication_cnt_array.append(0.0)

	#for delay
	#in successful transmission delay is caluclated as the difference between the time when sender sends data and the time receiver receives the data
	delay_time_send_array = np.zeros(1000) #should not be changed or initiazlied from the point of consistency
	delay_time_receive_array = np.zeros(1000) #should not be changed or initiazlied from the point of consistency
	delay_time_array = []

	#for jitter
	jitter_time_array = []

	#for energy
	TICKS_PER_SECOND = 32768
	EnergyTable      = []  # Energy:cpu,lpm,rx,tx,idle
	TmpTable         = []
	AVG=TOT=Cpu=Lpm=Tx=Rx=TOTtx=AVGtx=TOTtx=TOTrx=0.0
	tmp              = []

	dutycycle_array  = [] # added by Tada

	#------ line looping starts ------
	line_itr = 0 #to handle times, but stupid 
	for line in input_lines: #reversed is important to speed up
		#gathering data to variables
		if "Hello Tada" in line:
			if "Sending" in line:
				send += 1
				#for delay
				delay_time_send = float(line.split(" ")[4]) / 1000 #ms
				tmp_packet_id = int(line.split(" ")[12].split("\'")[0])
				delay_time_send_array[tmp_packet_id] = delay_time_send
			elif "received" in line:
				receive += 1
				#for delay
				delay_time_receive = float(line.split(" ")[4]) / 1000 #ms
				tmp_packet_id = int(line.split(" ")[12].split("\'")[0])
				delay_time_array.append(delay_time_receive - delay_time_send_array[tmp_packet_id])
				#for jitter
				if len(delay_time_array) > 1: #exclude the first packet
					jitter_time_array.append(abs(delay_time_array[len(delay_time_array)-1] - delay_time_array[len(delay_time_array)-2])) #difference of interarraval time
		elif "Replication" in line:
			replication += 1
			# tmp_split_line = line.split(" ")
			# temp_sid = int(tmp_split_line[2]) - 1
			# replication_cnt_array[temp_sid] += 1
		elif "Elimination" in line:
			elimination += 1
    #for calculating energy
		elif "PWR" in line:       #Cooja powertrace output "PowerF" in this example generaly is "P"
			tmp1 = line.split(" ")
			tmp1 = filter(None,tmp1)
			Cpu=Cpu+int(tmp1[15])             
			Lpm=Lpm+int(tmp1[16])
			Tx=Tx+int(tmp1[17])
			Rx=Rx+int(tmp1[18])

			tmp_duty_str = tmp1[22].split("%")[0]
			tmp_h_float = float(tmp_duty_str.split(".")[0])
			tmp_l_float = float(tmp_duty_str.split(".")[1])
			tmp_duty_value = tmp_h_float + tmp_l_float / 1000
			dutycycle_array.append(tmp_duty_value)

		#initializing variables or saving it it to arrays
		if ("start default" in line) or ("setedge" in line): #start resgistering
			if not "setedge" in input_lines[line_itr+1]: #first line in the event, time_counted_start already set
				time_counted_start = int(input_lines[line_itr+1].split(" ")[4])
				# print "---------- start ----------", time_counted_start
				#initialize variables
				pdr=send=receive=replication=elimination=0.0
				del delay_time_array[:]
				del jitter_time_array[:]
				#energy!!!
				EnergyTable      = []  # Energy:cpu,lpm,rx,tx,idle
				TmpTable         = []
				AVG=TOT=Cpu=Lpm=Tx=Rx=TOTtx=AVGtx=TOTtx=TOTrx=0.0
				tmp              = []

				del dutycycle_array[:]
		elif "report" in line: #finish regisetering and calculate data, put it into return array
			time_counted_end = int(input_lines[line_itr-1].split(" ")[4])
			# event_name = line.split(" ")[1].split("=")[1].split(",")[0] #old version! olala- dirty, but works
			event_name = line.split(" ")[2] + " " + line.split(" ")[3] #new version!
			if line.split(" ")[2] == 'def':
				event_name = 'o ' + line.split(" ")[3]
			elif line.split(" ")[2] == 'bad':
				event_name = 'x ' + line.split(" ")[3]
			# print "---------- end ----------", time_counted_end, event_name
			# print "time diff:", time_counted_end - time_counted_start
			#------------ calculating --------------
			#for time
			if INTERVAL_LINK_CHANGE > 0:
				counted_time_length_sec = INTERVAL_LINK_CHANGE
			else: 
				counted_time_length_sec = (time_counted_end - time_counted_start) / 1000 / 1000
			#for communication
			if send > 0:
				pdr = receive / send
			else:
				pdr = 0
			#for delay
			delay_avg = 0.0
			if len(delay_time_array) > 0:
				delay_avg = np.average(delay_time_array)
			#for jitter
			jitter_avg = 0.0
			if len(jitter_time_array) > 0:
				jitter_avg = np.average(jitter_time_array)
			#for efficiency
			efficiency = 0
			if delay_avg > 0:
				efficiency = pdr/delay_avg * 1000 #(%/s)

			#for energy
			TmpTable.insert(0, Cpu)
			TmpTable.insert(1, Lpm)
			TmpTable.insert(2, Tx)
			TmpTable.insert(3, Rx)
			for i in range(0,4):
				EnergyTable.append(float(TmpTable[i])/TICKS_PER_SECOND) #From ticks to seconds conversion                                                       
			#Calculating the Energy of each state(Cpu,lpm,tx,rx,idle=0)
			EnergyTable[0] = EnergyTable[0]* CURRENTS["power_cpu_mA"]*CURRENTS["voltage"]
			EnergyTable[1] = EnergyTable[1]* CURRENTS["power_lpm_mA"]*CURRENTS["voltage"]
			EnergyTable[2] = EnergyTable[2]* CURRENTS["power_tx_mA"] *CURRENTS["voltage"]
			EnergyTable[3] = EnergyTable[3]* CURRENTS["power_rx_mA"] *CURRENTS["voltage"]
			for i in range(0,4): #Adding them all together
			    AVG = EnergyTable[i] + AVG
			    TOT = EnergyTable[i] + TOT
			AVG = AVG/counted_time_length_sec #Calculating average power for n minutes of simulation here for 1 hour simulation(60-minutes)
			AVG_NODE = AVG/NUM_NODES

			dutycycle = np.average(dutycycle_array)

			# # print, print, print, print
			# print "event_name:", event_name,
			# print "pdr:", "{0:.2f}".format(pdr), 
			# print "s:", "{0:.0f}".format(send), "r:", "{0:.0f}".format(receive), 
			# print "rep:", "{0:.0f}".format(replication), "eli:", "{0:.0f}".format(elimination),
			# print "d(ms):", "{0:.0f}".format(delay_avg), 
			# print "j(ms):", "{0:.0f}".format(jitter_avg),
			# print "nrg(mW):", "{0:.2f}".format(AVG_NODE),
			# print "e(%/s):", "{0:.4f}".format(efficiency),
			# print ""

			# # detailed print 
			# print "replication:", replication, "elimination:", elimination
			# print "TOT_NET(mj):", TOT, "AVG_NET(mW):", AVG, "TOT_NODE(mj):", TOT/NUM_NODES, "AVG_NODE(mW):", AVG/NUM_NODES
			# print "counted_time_length_sec", counted_time_length_sec
			# print "replication_cnt_array: ",	
			# for i in range(0, NUM_NODES):
			# 	print str(i+1) + ":", str(replication_cnt_array[i]),
			# print ""
			# print "total replication:", str(sum(replication_cnt_arrnay))
			 
			#---------------saving to arrays------------
			new_dict = {"event_id" : r_event_id}
			new_dict["name"] = event_name
			new_dict["pdr"] = pdr
			new_dict["rep"] = replication
			new_dict["eli"] = elimination
			new_dict["delay"] = delay_avg
			new_dict["jitter"] = jitter_avg
			new_dict["energy"] = AVG_NODE
			new_dict["efficiency"] = efficiency
			new_dict["dutycycle"] = dutycycle
			r_array.append(new_dict)
			r_event_id += 1
		
		line_itr += 1 #this is sooooooooooo important to get time.

	#------- input line looping finished------
	return r_array #return array of dictionary.

def get_graph_array_from_data(datapath, directory_name, sim_cnt_min, sim_cnt_max): #for REALSIM, return[0] = graph_array, return[1] = directory_name
# return data in following array structure from all simulation result files in same configration (leapfrog, normal,...)
#  [[sim1, sim2, sim3, ...], directory_name]
#    sim = [[event1, event2, event3,...], sim_cnt]
#    event = dict of {"event_id", "name", "pdr", "rep", "eli", "delay", "jitter", "energy", "efficiency",...}
  cnt_skip = 0
  cnt_data = 0
  result_array = []
  #gather data for each different random seeds
  for sim_cnt in range(sim_cnt_min, sim_cnt_max+1):
    # print sim_cnt
    input_file_name = datapath + directory_name + "/" + str(sim_cnt) + "/" + "COOJA.testlog"
    result = get_result_from_file_realsim(input_file_name)
    if result is None:
      cnt_skip += 1
      continue #if no data, skip
    result_array.append([result, sim_cnt])
    cnt_data += 1
  print directory_name, "cnt_data", cnt_data, "cnt_skip", cnt_skip
  return result_array, directory_name

	
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# -=-=-=-=-=-= test main =-=-=-=-=-=-
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

if __name__ == "__main__":
	# input_file_name = "C:/Users/Tada/Documents/Telecom_local/arrange_result_realsim/scenario2/normal/1/COOJA.testlog" # input file for COOJA.testlog
	input_file_name = "C:/Users/Tada/Documents/Telecom_local/arrange_result_realsim/scenario4/normal/18/COOJA.testlog" # input file for COOJA.testlog
	result = get_result_from_file_realsim(input_file_name)
	print result[0]["event_id"]
	print result[1]["jitter"]
	print result[2]["event_id"]

