#python script file for extracting data from Cooja simulation result
#put this file in the same directory where "leapfrog" "normal" etc... exist

#This script is for the result with DGRM configuration as a radio medium

import numpy as np
import matplotlib.pyplot as plt
import csv

#parameters for targt files
sim_cnt_max = 20
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

# -------------------functions------------------
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

	#for jitter
	#in successful transmission jitter is caluclated as the difference between the time when sender sends data and the time receiver receives the data
	jitter_time_send_array = np.zeros(1000)
	jitter_time_receive_array = np.zeros(1000)
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
					#for jitter
					tmp_split_line = line.split(" ")
					jitter_time_send = float(tmp_split_line[4]) / 1000 #ms
					tmp_str = tmp_split_line[12].split("\'")
					tmp_packet_id = int(tmp_str[0])
					jitter_time_send_array[tmp_packet_id] = jitter_time_send

				elif "received" in line:
					receive += 1
					#for jitter
					tmp_split_line = line.split(" ")
					jitter_time_receive = float(tmp_split_line[4]) / 1000 #ms
					tmp_str = tmp_split_line[20].split("\'")
					tmp_packet_id = int(tmp_str[0])
					jitter_time_array.append(jitter_time_receive - jitter_time_send_array[tmp_packet_id])

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

	#for jitter
	jitter_avg = 0.0
	if len(jitter_time_array) > 0:
		jitter_avg = np.average(jitter_time_array)

	#print
	print "pdr:", pdr, "send:", send, "receive:", receive,"replication:", replication, "elimination:", elimination
	print "TOT_NET(mj):", TOT, "AVG_NET(mW):", AVG, "TOT_NODE(mj):", TOT/NUM_NODES, "AVG_NODE(mW):", AVG/NUM_NODES
	print "jitter(ms):", jitter_avg
	return (pdr, send, receive, replication, elimination, TOT, AVG, TOT/NUM_NODES, AVG/NUM_NODES, jitter_avg)

def get_graph_array_from_data(directory_name):
	#array for graphs
	pdr_graph_array = []
	send_graph_array = []
	receive_graph_array = []
	replication_graph_array = []
	elimination_graph_array = []
	nrg_net_total_graph_array = []
	nrg_net_avg_graph_array = []
	delay_graph_array = []
	jitter_graph_array = []

	pdr_array = []
	send_array = []
	receive_array = []
	replication_array = []
	elimination_array = []
	nrg_net_total_array = []
	nrg_net_avg_array = []
	delay_array = []
	jitter_array = []
	#gather data for each different random seeds
	for sim_cnt in range(sim_cnt_min, sim_cnt_max+1):
		print sim_cnt
		input_file_name = "./" + directory_name + "/" + str(sim_cnt) + "/" + "COOJA.testlog"
		result = get_result_from_file(input_file_name)
		pdr_array.append(result[0])
		send_array.append(result[1])
		receive_array.append(result[2])
		replication_array.append(result[3])
		elimination_array.append(result[4])
		nrg_net_total_array.append(result[5])
		nrg_net_avg_array.append(result[6])
		delay_array.append(result[9])
		jitter_array.append(result[10])

	#for graphs
	pdr_graph_array.append(pdr_array)
	send_graph_array.append(send_array)
	receive_graph_array.append(receive_array)
	replication_graph_array.append(replication_array)
	elimination_graph_array.append(elimination_array)
	nrg_net_total_graph_array.append(nrg_net_total_array)
	nrg_net_avg_graph_array.append(nrg_net_avg_array)
	delay_graph_array.append(delay_array)
	jitter_graph_array.append(jitter_array)

	return [pdr_graph_array, send_graph_array, receive_graph_array, replication_graph_array, elimination_graph_array, nrg_net_total_graph_array, nrg_net_avg_graph_array, delay_graph_array, jitter_graph_array]

def set_boxplot_color(bp, color_name, hatch_name):
	bp['boxes'][0].set(edgecolor=color_name, hatch=hatch_name)
	bp['medians'][0].set(color=color_name)
	bp['caps'][0].set(color=color_name) #width of upper line
	bp['caps'][1].set(color=color_name) #width of lower line
	bp['whiskers'][0].set(color=color_name) #width to upper line
	bp['whiskers'][1].set(color=color_name) #width to lower linr

#-------------------------- main start -------------------------------

#--------------arrange data -------------------
print "---------------------------------"
print "-try to arrange data from Normal-"
print "---------------------------------"

result = get_graph_array_from_data("normal")
pdr_no = result[0]
send_no = result[1]
receive_no = result[2]
replication_no = result[3]
elimination_no = result[4]
nrg_net_total_no = result[5]
nrg_net_avg_no = result[6]
delay_no = result[7]
jitter_no = result[8]

print "---------------------------------"
print "-try to arrange data from Leapfrog-"
print "---------------------------------"

result = get_graph_array_from_data("leapfrog")
pdr_lf = result[0]
send_lf = result[1]
receive_lf = result[2]
replication_lf = result[3]
elimination_lf = result[4]
nrg_net_total_lf = result[5]
nrg_net_avg_lf = result[6]
delay_lf = result[7]
jitter_lf = result[8]

print "---------------------------------"
print "-try to arrange data from Normal ReTx-2-"
print "---------------------------------"

result = get_graph_array_from_data("normal-re2")
pdr_re2 = result[0]
send_re2 = result[1]
receive_re2 = result[2]
replication_re2 = result[3]
elimination_re2 = result[4]
nrg_net_total_re2 = result[5]
nrg_net_avg_re2 = result[6]
delay_re2 = result[7]
jitter_re2 = result[8]

print "---------------------------------"
print "-try to arrange data from Normal ReTx-4-"
print "---------------------------------"

result = get_graph_array_from_data("normal-re4")
pdr_re4 = result[0]
send_re4 = result[1]
receive_re4 = result[2]
replication_re4 = result[3]
elimination_re4 = result[4]
nrg_net_total_re4 = result[5]
nrg_net_avg_re4 = result[6]
delay_re4 = result[7]
jitter_re4 = result[8]

print "---------------------------------"
print "-try to arrange data from Normal ReTx-6-"
print "---------------------------------"

result = get_graph_array_from_data("normal-re6")
pdr_re6 = result[0]
send_re6 = result[1]
receive_re6 = result[2]
replication_re6 = result[3]
elimination_re6 = result[4]
nrg_net_total_re6 = result[5]
nrg_net_avg_re6 = result[6]
delay_re6 = result[7]
jitter_re6 = result[8]

print "---------------------------------"
print "-try to arrange data from Normal ReTx-8-"
print "---------------------------------"

result = get_graph_array_from_data("normal-re8")
pdr_re8 = result[0]
send_re8 = result[1]
receive_re8 = result[2]
replication_re8 = result[3]
elimination_re8 = result[4]
nrg_net_total_re8 = result[5]
nrg_net_avg_re8 = result[6]
delay_re8 = result[7]
jitter_re8 = result[8]

#--------------plot color and textures---------------
color_no = ['blue', '/']
color_lf = ['green', '\\']
color_re2 = ['red', '*']
color_re4 = ['cyan', 'o']
color_re6 = ['magenta', 'O']
color_re8 = ['yellow', '.']

#--------------PDR boxplot-------------
fig, ax = plt.subplots()

i = 0 # for i in range(10):
xticks = []
xticks.append('')

xticks.append('no')
bp = plt.boxplot(pdr_no[i], positions=[i + len(xticks)-1], patch_artist=True)
set_boxplot_color(bp, color_no[0], color_no[1])
xticks.append('re2')
bp = plt.boxplot(pdr_re2[i], positions=[i + len(xticks)-1], patch_artist=True)
set_boxplot_color(bp, color_re2[0], color_re2[1])
xticks.append('re4')
bp = plt.boxplot(pdr_re4[i], positions=[i + len(xticks)-1], patch_artist=True)
set_boxplot_color(bp, color_re4[0], color_re4[1])
xticks.append('re6')
bp = plt.boxplot(pdr_re6[i], positions=[i + len(xticks)-1], patch_artist=True)
set_boxplot_color(bp, color_re6[0], color_re6[1])
xticks.append('re8')
bp = plt.boxplot(pdr_re8[i], positions=[i + len(xticks)-1], patch_artist=True)
set_boxplot_color(bp, color_re8[0], color_re8[1])
xticks.append('lf')
bp = plt.boxplot(pdr_lf[i], positions=[i + len(xticks)-1], patch_artist=True)
set_boxplot_color(bp, color_lf[0], color_lf[1])

#xticks
plt.xticks([i for i in range(0, len(xticks))], xticks, rotation=0) #must be changed correpoiding to the number of data

#only used for making legends
ax.bar([1], [0], color='white', edgecolor=color_no[0], hatch=color_no[1], label='default ReTx=0')
ax.bar([1], [0], color='white', edgecolor=color_re2[0], hatch=color_re2[1], label='default ReTx=2')
ax.bar([1], [0], color='white', edgecolor=color_re4[0], hatch=color_re4[1], label='default ReTx=4')
ax.bar([1], [0], color='white', edgecolor=color_re6[0], hatch=color_re6[1], label='default ReTx=6')
ax.bar([1], [0], color='white', edgecolor=color_re8[0], hatch=color_re8[1], label='default ReTx=8')
ax.bar([1], [0], color='white', edgecolor=color_lf[0], hatch=color_lf[1], label='Leapfrog Collaboration')

plt.legend(ncol=2, loc='lower left')
# ax.set_xlabel('Link quality (%)')
ax.set_ylabel('Packet Delivery Ratio (%)')

fig.savefig("pdr" + ".png")

#--------------Energy boxplot-------------
fig, ax = plt.subplots()

i = 0 # for i in range(10):
xticks = []
xticks.append('')

xticks.append('no')
bp = plt.boxplot(nrg_net_avg_no[i], positions=[i + len(xticks)-1], patch_artist=True)
set_boxplot_color(bp, color_no[0], color_no[1])
xticks.append('re2')
bp = plt.boxplot(nrg_net_avg_re2[i], positions=[i + len(xticks)-1], patch_artist=True)
set_boxplot_color(bp, color_re2[0], color_re2[1])
xticks.append('re4')
bp = plt.boxplot(nrg_net_avg_re4[i], positions=[i + len(xticks)-1], patch_artist=True)
set_boxplot_color(bp, color_re4[0], color_re4[1])
xticks.append('re6')
bp = plt.boxplot(nrg_net_avg_re6[i], positions=[i + len(xticks)-1], patch_artist=True)
set_boxplot_color(bp, color_re6[0], color_re6[1])
xticks.append('re8')
bp = plt.boxplot(nrg_net_avg_re8[i], positions=[i + len(xticks)-1], patch_artist=True)
set_boxplot_color(bp, color_re8[0], color_re8[1])
xticks.append('lf')
bp = plt.boxplot(nrg_net_avg_lf[i], positions=[i + len(xticks)-1], patch_artist=True)
set_boxplot_color(bp, color_lf[0], color_lf[1])

#xticks
plt.xticks([i for i in range(0, len(xticks))], xticks, rotation=0) #must be changed correpoiding to the number of data

#only used for making legends
ax.bar([1], [0], color='white', edgecolor=color_no[0], hatch=color_no[1], label='default ReTx=0')
ax.bar([1], [0], color='white', edgecolor=color_re2[0], hatch=color_re2[1], label='default ReTx=2')
ax.bar([1], [0], color='white', edgecolor=color_re4[0], hatch=color_re4[1], label='default ReTx=4')
ax.bar([1], [0], color='white', edgecolor=color_re6[0], hatch=color_re6[1], label='default ReTx=6')
ax.bar([1], [0], color='white', edgecolor=color_re8[0], hatch=color_re8[1], label='default ReTx=8')
ax.bar([1], [0], color='white', edgecolor=color_lf[0], hatch=color_lf[1], label='Leapfrog Collaboration')

plt.legend(ncol=2, loc='upper left')
# ax.set_xlabel('Link quality (%)')
ax.set_ylabel('Average energy consumption of network (mA)')
ax.set_ylim(6, 11)

fig.savefig("nrg" + ".png")

#--------------delay boxplot-------------
fig, ax = plt.subplots()

i = 0 # for i in range(10):
xticks = []
xticks.append('')

xticks.append('no')
bp = plt.boxplot(delay_no[i], positions=[i + len(xticks)-1], patch_artist=True)
set_boxplot_color(bp, color_no[0], color_no[1])
xticks.append('re2')
bp = plt.boxplot(delay_re2[i], positions=[i + len(xticks)-1], patch_artist=True)
set_boxplot_color(bp, color_re2[0], color_re2[1])
xticks.append('re4')
bp = plt.boxplot(delay_re4[i], positions=[i + len(xticks)-1], patch_artist=True)
set_boxplot_color(bp, color_re4[0], color_re4[1])
xticks.append('re6')
bp = plt.boxplot(delay_re6[i], positions=[i + len(xticks)-1], patch_artist=True)
set_boxplot_color(bp, color_re6[0], color_re6[1])
xticks.append('re8')
bp = plt.boxplot(delay_re8[i], positions=[i + len(xticks)-1], patch_artist=True)
set_boxplot_color(bp, color_re8[0], color_re8[1])
xticks.append('lf')
bp = plt.boxplot(delay_lf[i], positions=[i + len(xticks)-1], patch_artist=True)
set_boxplot_color(bp, color_lf[0], color_lf[1])

#xticks
plt.xticks([i for i in range(0, len(xticks))], xticks, rotation=0) #must be changed correpoiding to the number of data

#only used for making legends
ax.bar([1], [0], color='white', edgecolor=color_no[0], hatch=color_no[1], label='default ReTx=0')
ax.bar([1], [0], color='white', edgecolor=color_re2[0], hatch=color_re2[1], label='default ReTx=2')
ax.bar([1], [0], color='white', edgecolor=color_re4[0], hatch=color_re4[1], label='default ReTx=4')
ax.bar([1], [0], color='white', edgecolor=color_re6[0], hatch=color_re6[1], label='default ReTx=6')
ax.bar([1], [0], color='white', edgecolor=color_re8[0], hatch=color_re8[1], label='default ReTx=8')
ax.bar([1], [0], color='white', edgecolor=color_lf[0], hatch=color_lf[1], label='Leapfrog Collaboration')

plt.legend(ncol=2, loc='lower left')
# ax.set_xlabel('Link quality (%)')
ax.set_ylabel('delay (ms)')
ax.set_ylim(0, 15000)

fig.savefig("delay" + ".png")

#--------------jitter boxplot-------------
fig, ax = plt.subplots()

i = 0 # for i in range(10):
xticks = []
xticks.append('')

xticks.append('no')
bp = plt.boxplot(jitter_no[i], positions=[i + len(xticks)-1], patch_artist=True)
set_boxplot_color(bp, color_no[0], color_no[1])
xticks.append('re2')
bp = plt.boxplot(jitter_re2[i], positions=[i + len(xticks)-1], patch_artist=True)
set_boxplot_color(bp, color_re2[0], color_re2[1])
xticks.append('re4')
bp = plt.boxplot(jitter_re4[i], positions=[i + len(xticks)-1], patch_artist=True)
set_boxplot_color(bp, color_re4[0], color_re4[1])
xticks.append('re6')
bp = plt.boxplot(jitter_re6[i], positions=[i + len(xticks)-1], patch_artist=True)
set_boxplot_color(bp, color_re6[0], color_re6[1])
xticks.append('re8')
bp = plt.boxplot(jitter_re8[i], positions=[i + len(xticks)-1], patch_artist=True)
set_boxplot_color(bp, color_re8[0], color_re8[1])
xticks.append('lf')
bp = plt.boxplot(jitter_lf[i], positions=[i + len(xticks)-1], patch_artist=True)
set_boxplot_color(bp, color_lf[0], color_lf[1])

#xticks
plt.xticks([i for i in range(0, len(xticks))], xticks, rotation=0) #must be changed correpoiding to the number of data

#only used for making legends
ax.bar([1], [0], color='white', edgecolor=color_no[0], hatch=color_no[1], label='default ReTx=0')
ax.bar([1], [0], color='white', edgecolor=color_re2[0], hatch=color_re2[1], label='default ReTx=2')
ax.bar([1], [0], color='white', edgecolor=color_re4[0], hatch=color_re4[1], label='default ReTx=4')
ax.bar([1], [0], color='white', edgecolor=color_re6[0], hatch=color_re6[1], label='default ReTx=6')
ax.bar([1], [0], color='white', edgecolor=color_re8[0], hatch=color_re8[1], label='default ReTx=8')
ax.bar([1], [0], color='white', edgecolor=color_lf[0], hatch=color_lf[1], label='Leapfrog Collaboration')

plt.legend(ncol=2, loc='upper right')
# ax.set_xlabel('Link quality (%)')
ax.set_ylabel('jitter (ms)')
ax.set_ylim(30000, 80000)

fig.savefig("jitter" + ".png")

#---------------fin and show -------------
plt.show()