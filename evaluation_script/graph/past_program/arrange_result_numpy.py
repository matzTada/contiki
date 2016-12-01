#python script file for extracting data from Cooja simulation result
#put this file in the same directory where "Tx-Rx" folder(s) exist(s)

import numpy as np

def get_result_from_file(input_file_name): #get result from indicated file
	input_file = open(input_file_name)
	input_lines = input_file.readlines()
	input_file.close

	for line in reversed(input_lines): #reversed is important to speed up
		if "Simulation time expired" in line:
			#print line,
			data = line.split(" ")
			pdr = 0.0
			send = 0
			receive = 0
			replication = 0
			elimination = 0
			for i in range(0, len(data) - 1):
				tmp = str(data[i+1])
				if tmp == "NaN":
					tmp = str(0)

				if data[i] == "PDR":
					pdr = float(tmp)
				elif data[i] == "#send":
					send = int(tmp)
				elif data[i] == "#receive":
					receive = int(tmp)
				elif data[i] == "#replication":
					replication = int(tmp)
				elif data[i] == "#elimination":
					elimination = int(tmp)
			print "pdr", pdr, "send", send, "receive", receive,"replication", replication, "elimination", elimination
			return (pdr, send, receive, replication, elimination)	

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
rx_min = 10
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
	for rx in range(rx_min, rx_max+1, rx_step):
		pdr_array = []
		send_array = []
		receive_array = []
		replication_array = []
		elimination_array = []
		for sim_cnt in range(sim_cnt_min, sim_cnt_max+1):
			print tx, "-", rx, "-", sim_cnt, 
			input_file_name = "./" + str(tx) + "-" + str(rx) + "/" + str(sim_cnt) + "/" + "COOJA.testlog"
			result = get_result_from_file(input_file_name)
			pdr_array.append(result[0])
			send_array.append(result[1])
			receive_array.append(result[2])
			replication_array.append(result[3])
			elimination_array.append(result[4])
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
	
print output_str
output_result_to_file("result_arranged.csv", output_str)
