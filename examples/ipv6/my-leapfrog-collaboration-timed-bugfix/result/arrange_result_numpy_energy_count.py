#python script file for extracting data from Cooja simulation result
#put this file in the same directory where "Tx-Rx" folder(s) exist(s)

import numpy as np
import csv

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
	replication_cnt_for_node = 0.0;

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
		if line.find(" P ") > 0:       #Cooja powertrace output "PowerF" in this example generaly is "P"
			tmp1 = line.split(" ")
			tmp1 = filter(None,tmp1)
			Cpu=Cpu+int(tmp1[15])             
			Lpm=Lpm+int(tmp1[16])
			Tx=Tx+int(tmp1[17])
			Rx=Rx+int(tmp1[18])
		
		if "Hello Tada" in line:
			if not (("Hello TadaMatz 0" in line) or ("Hello Tada 0000" in line)):
				if "Sending" in line:
					send += 1
				elif "received" in line:
					receive += 1
		if "Replication" in line:
			replication += 1
		elif "Elimination" in line:
			elimination += 1

		#to calculate number of replication on specific node
		#if "Rep: ID: 6" in line:
		#	replication_cnt_for_node += 1
	
		#read the line showing result
		#if "Simulation time expired" in line:
		#	print line,
		#	data = line.split(" ")
		#	for i in range(0, len(data) - 1):
		#		tmp = str(data[i+1])
		#		if tmp == "NaN":
		#			tmp = str(0)
		#
		#		if data[i] == "PDR":
		#			pdr = float(tmp)
		#		elif data[i] == "#send":
		#			send = int(tmp)
		#		elif data[i] == "#receive":
		#			receive = int(tmp)
		#		elif data[i] == "#replication":
		#			replication = int(tmp)
		#		elif data[i] == "#elimination":
		#			elimination = int(tmp)
	
	#for time
	counted_time_length_sec = (time_counted_end - time_counted_start) / 1000 / 1000
	print "counted_time_length_sec", counted_time_length_sec

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

	#print
	print "pdr", pdr, "send", send, "receive", receive,"replication", replication, "elimination", elimination
	print "TOT_NET(mj)", TOT, "AVG_NET(mW)", AVG, "TOT_NODE(mj)", TOT/NUM_NODES, "AVG_NODE(mW)", AVG/NUM_NODES
	#print "replication_cnt_for_node", replication_cnt_for_node
	return (pdr, send, receive, replication, elimination, TOT, AVG, TOT/NUM_NODES, AVG/NUM_NODES, replication_cnt_for_node)	

def output_result_to_file(name, result_str):
	try:
		output = open(name, "w")
		output.write(result_str)
		print "Output data to", name
	except:
		print "Output faild. exit"
	finally:
		output.close()
	
#-------------------------- main start -------------------------------

tx_max = 100
tx_min = 100
tx_step = 10
rx_max = 100
rx_min = 90
rx_step = 10
sim_cnt_max = 3
sim_cnt_min = 1

pdr_avg_str = "tx|rx->,"
pdr_var_str = "tx|rx->,"
send_avg_str = "tx|rx->,"
send_var_str = "tx|rx->,"
receive_avg_str = "tx|rx->,"
receive_var_str = "tx|rx->,"
replication_avg_str = "tx|rx->,"
replication_var_str = "tx|rx->,"
elimination_avg_str = "tx|rx->,"
elimination_var_str = "tx|rx->,"
nrg_net_total_avg_str = "tx|rx->,"
nrg_net_total_var_str = "tx|rx->,"
nrg_net_avg_avg_str = "tx|rx->,"
nrg_net_avg_var_str = "tx|rx->,"

#initialize str
for rx in range(rx_min, rx_max+1, rx_step): #make label
	pdr_avg_str += str(rx) + ","
	pdr_var_str += str(rx) + ","
	send_avg_str += str(rx) + ","
	send_var_str += str(rx) + ","
	receive_avg_str += str(rx) + ","
	receive_var_str += str(rx) + ","
	replication_avg_str += str(rx) + ","
	replication_var_str += str(rx) + ","
	elimination_avg_str += str(rx) + ","
	elimination_var_str += str(rx) + ","
	nrg_net_total_avg_str += str(rx) + ","
	nrg_net_total_var_str += str(rx) + ","
	nrg_net_avg_avg_str += str(rx) + ","
	nrg_net_avg_var_str += str(rx) + ","

for tx in range(tx_min, tx_max+1, tx_step):
	pdr_avg_str += "\n" + str(tx) + ","
	pdr_var_str += "\n" + str(tx) + ","
	send_avg_str += "\n" + str(tx) + ","
	send_var_str += "\n" + str(tx) + ","
	receive_avg_str += "\n" + str(tx) + ","
	receive_var_str += "\n" + str(tx) + ","
	replication_avg_str += "\n" + str(tx) + ","
	replication_var_str += "\n" + str(tx) + ","
	elimination_avg_str += "\n" + str(tx) + ","
	elimination_var_str += "\n" + str(tx) + ","
	nrg_net_total_avg_str += "\n" + str(tx) + ","
	nrg_net_total_var_str += "\n" + str(tx) + ","
	nrg_net_avg_avg_str += "\n" + str(tx) + ","
	nrg_net_avg_var_str += "\n" + str(tx) + ","
	for rx in range(rx_min, rx_max+1, rx_step):
		pdr_array = []
		send_array = []
		receive_array = []
		replication_array = []
		elimination_array = []
		nrg_net_total_array = []
		nrg_net_avg_array = []
		for sim_cnt in range(sim_cnt_min, sim_cnt_max+1):
			print tx, "-", rx, "-", sim_cnt
			input_file_name = "./" + str(tx) + "-" + str(rx) + "/" + str(sim_cnt) + "/" + "COOJA.testlog"
			result = get_result_from_file(input_file_name)
			pdr_array.append(result[0])
			send_array.append(result[1])
			receive_array.append(result[2])
			replication_array.append(result[3])
			elimination_array.append(result[4])
			nrg_net_total_array.append(result[5])
			nrg_net_avg_array.append(result[6])
		pdr_avg_str += str(np.average(pdr_array)) + ","
		pdr_var_str += str(np.std(pdr_array)) + ","
		send_avg_str += str(np.average(send_array)) + ","
		send_var_str += str(np.std(send_array)) + ","
		receive_avg_str += str(np.average(receive_array)) + ","
		receive_var_str += str(np.std(receive_array)) + ","
		replication_avg_str += str(np.average(replication_array)) + ","
		replication_var_str += str(np.std(replication_array)) + ","
		elimination_avg_str += str(np.average(elimination_array)) + ","
		elimination_var_str += str(np.std(elimination_array)) + ","
		nrg_net_total_avg_str += str(np.average(nrg_net_total_array)) + ","
		nrg_net_total_var_str += str(np.std(nrg_net_total_array)) + ","
		nrg_net_avg_avg_str += str(np.average(nrg_net_avg_array)) + ","
		nrg_net_avg_var_str += str(np.std(nrg_net_avg_array)) + ","
	
output_str = ""	

output_str += "\n" + "pdr_avg_str" + "\n" + pdr_avg_str + "\n"
output_str += "\n" + "pdr_var_str" + "\n" + pdr_var_str + "\n"
output_str += "\n" + "send_avg_str" + "\n" + send_avg_str + "\n"
output_str += "\n" + "send_var_str" + "\n" + send_var_str + "\n"
output_str += "\n" + "receive_avg_str" + "\n" + receive_avg_str + "\n"
output_str += "\n" + "receive_var_str" + "\n" + receive_var_str + "\n"
output_str += "\n" + "replication_avg_str" + "\n" + replication_avg_str + "\n"
output_str += "\n" + "replication_var_str" + "\n" + replication_var_str + "\n"
output_str += "\n" + "elimination_avg_str" + "\n" + elimination_avg_str + "\n"
output_str += "\n" + "elimination_var_str" + "\n" + elimination_var_str + "\n"

output_str += "\n" + "nrg_net_total_avg_str" + "\n" + nrg_net_total_avg_str + "\n"
output_str += "\n" + "nrg_net_total_var_str" + "\n" + nrg_net_total_var_str + "\n"
output_str += "\n" + "nrg_net_avg_avg_str" + "\n" + nrg_net_avg_avg_str + "\n"
output_str += "\n" + "nrg_net_avg_var_str" + "\n" + nrg_net_avg_var_str + "\n"
	
print output_str
output_result_to_file("result_arranged.csv", output_str)
