#python script file for extracting data from Cooja simulation result
#put this file in the same directory where "Tx-Rx" folder(s) exist(s)

import numpy as np
import matplotlib.pyplot as plt
import csv

#parameter
tx_max = 100
tx_min = 100
tx_step = 10
rx_max = 100
rx_min = 10
rx_step = 10
sim_cnt_max = 3
sim_cnt_min = 1

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
				elif "received" in line:
					receive += 1
		if ("Replication" in line) and (first_hello_flag == 1):
			tmp_split_line = line.split(" ")
			temp_sid = int(tmp_split_line[2]) - 1
			replication_cnt_array[temp_sid] += 1
			replication += 1
		elif ("Elimination" in line) and (first_hello_flag == 1):
			elimination += 1
	
	#for time
	counted_time_length_sec = (time_counted_end - time_counted_start) / 1000 / 1000
	print "counted_time_length_sec", counted_time_length_sec

	#for communication
	if send > 0:
		pdr = receive / send
	else:
		pdr = 0
	
	#for replication
	print "replication_cnt_array: ",	
	for i in range(0, NUM_NODES):
		print str(i+1) + ":", str(replication_cnt_array[i]),
	print ""
	print "total replication:", str(sum(replication_cnt_array))

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

	#print
	print "pdr:", pdr, "send:", send, "receive:", receive,"replication:", replication, "elimination:", elimination
	print "TOT_NET(mj):", TOT, "AVG_NET(mW):", AVG, "TOT_NODE(mj):", TOT/NUM_NODES, "AVG_NODE(mW):", AVG/NUM_NODES
	print "Jitter(ms):"
	return (pdr, send, receive, replication, elimination, TOT, AVG, TOT/NUM_NODES, AVG/NUM_NODES)	


def set_boxplot_color(bp, color_name, hatch_name):
	bp['boxes'][0].set(edgecolor=color_name, hatch=hatch_name)
	bp['medians'][0].set(color=color_name)
	bp['caps'][0].set(color=color_name) #width of upper line
	bp['caps'][1].set(color=color_name) #width of lower line
	bp['whiskers'][0].set(color=color_name) #width to upper line
	bp['whiskers'][1].set(color=color_name) #width to lower linr

#-------------------------- main start -------------------------------

print "---------------------------------"
print "-try to arrange data from Normal-"
print "---------------------------------"
#array for graphs
pdr_graph_array = []
send_graph_array = []
receive_graph_array = []
replication_graph_array = []
elimination_graph_array = []
nrg_net_total_graph_array = []
nrg_net_avg_graph_array = []

for tx in range(tx_min, tx_max+1, tx_step):
	for rx in range(rx_min, rx_max+1, rx_step):
		pdr_array = []
		send_array = []
		receive_array = []
		replication_array = []
		elimination_array = []
		nrg_net_total_array = []
		nrg_net_avg_array = []
		#gather data for each different random seeds
		for sim_cnt in range(sim_cnt_min, sim_cnt_max+1):
			print tx, "-", rx, "-", sim_cnt
			input_file_name = "./normal/" + str(tx) + "-" + str(rx) + "/" + str(sim_cnt) + "/" + "COOJA.testlog"
			result = get_result_from_file(input_file_name)
			pdr_array.append(result[0])
			send_array.append(result[1])
			receive_array.append(result[2])
			replication_array.append(result[3])
			elimination_array.append(result[4])
			nrg_net_total_array.append(result[5])
			nrg_net_avg_array.append(result[6])

		#for graphs
		pdr_graph_array.append(pdr_array)
		send_graph_array.append(send_array)
		receive_graph_array.append(receive_array)
		replication_graph_array.append(replication_array)
		elimination_graph_array.append(elimination_array)
		nrg_net_total_graph_array.append(nrg_net_total_array)
		nrg_net_avg_graph_array.append(nrg_net_avg_array)

pdr_no = pdr_graph_array
send_no = send_graph_array
receive_no = receive_graph_array
replication_no = replication_graph_array
elimination_no = elimination_graph_array
nrg_net_total_no = nrg_net_total_graph_array
nrg_net_avg_no = nrg_net_avg_graph_array


print "---------------------------------"
print "-try to arrange data from Leapfrog-"
print "---------------------------------"
#array for graphs
pdr_graph_array = []
send_graph_array = []
receive_graph_array = []
replication_graph_array = []
elimination_graph_array = []
nrg_net_total_graph_array = []
nrg_net_avg_graph_array = []

for tx in range(tx_min, tx_max+1, tx_step):
	for rx in range(rx_min, rx_max+1, rx_step):
		pdr_array = []
		send_array = []
		receive_array = []
		replication_array = []
		elimination_array = []
		nrg_net_total_array = []
		nrg_net_avg_array = []
		#gather data for each different random seeds
		for sim_cnt in range(sim_cnt_min, sim_cnt_max+1):
			print tx, "-", rx, "-", sim_cnt
			input_file_name = "./leapfrog/" + str(tx) + "-" + str(rx) + "/" + str(sim_cnt) + "/" + "COOJA.testlog"
			result = get_result_from_file(input_file_name)
			pdr_array.append(result[0])
			send_array.append(result[1])
			receive_array.append(result[2])
			replication_array.append(result[3])
			elimination_array.append(result[4])
			nrg_net_total_array.append(result[5])
			nrg_net_avg_array.append(result[6])

		#for graphs
		pdr_graph_array.append(pdr_array)
		send_graph_array.append(send_array)
		receive_graph_array.append(receive_array)
		replication_graph_array.append(replication_array)
		elimination_graph_array.append(elimination_array)
		nrg_net_total_graph_array.append(nrg_net_total_array)
		nrg_net_avg_graph_array.append(nrg_net_avg_array)

pdr_lf = pdr_graph_array
send_lf = send_graph_array
receive_lf = receive_graph_array
replication_lf = replication_graph_array
elimination_lf = elimination_graph_array
nrg_net_total_lf = nrg_net_total_graph_array
nrg_net_avg_lf = nrg_net_avg_graph_array

#start to plot pdr
fig, ax = plt.subplots()

color_no = 'blue'
color_lf = 'green'

for i in range(10):
	bp1 = plt.boxplot(pdr_no[i], positions=[2*i+1], widths=0.8, patch_artist=True)
	set_boxplot_color(bp1, color_no, '/')

	bp2 = plt.boxplot(pdr_lf[i], positions=[2*i+2], widths=0.8, patch_artist=True)
	set_boxplot_color(bp2, color_lf, '//')

#xticks
xticks = []
for i in range(10):
	xticks.append('')
	xticks.append(str(i+1))

plt.xticks([i for i in range(20)], xticks)

#legends
banana, = plt.plot([1,1], color_no, label='Normal')
cucumber, = plt.plot([1,1], color_lf, label='Leapfrog')
plt.legend(loc='upper right')
banana.set_visible(False)
cucumber.set_visible(False)

# fig = plt.figure()
# ax1 = fig.add_subplot(111)
# ax1.boxplot(pdr_no)
# ax1.boxplot(pdr_lf)
# ax1.xticks([1,2,3,4,5,6,7,8,9,10], [10, 20, 30, 40, 50, 60, 70, 80, 90, 100])

# ax2 = ax1.twinx()
# ax2.boxplot(nrg_net_avg_no)
# ax2.boxplot(nrg_net_avg_lf)

plt.show()