#python script file for extracting data from Cooja simulation result
#put this file in the same directory where "Tx-Rx" folder(s) exist(s)

#This script is for the result with DGRM configuration as a radio medium

import numpy as np
import matplotlib.pyplot as plt
import csv

from mod_getdata import get_result_from_file, get_randomseed_from_file, set_boxplot_color

#data path
# datapath = "C:/Users/Tada/Documents/Telecom_local/arrange_result2nd-overhear-udgm/" 
# datapath = "C:/Users/Tada/Documents/Telecom_local/arrange_result2nd-overhear-udgm-2/" 
# datapath = "C:/Users/Tada/Documents/Telecom_local/frag_result-overhear-udgm-3/" 
# datapath = "C:/Users/Tada/Documents/Telecom_local/frag_result-overhear-udgm-4/" 
# datapath = "C:/Users/Tada/Documents/Telecom_local/arrange_result2nd-UDGM/" 
# datapath = "C:/Users/Tada/Documents/Telecom_local/arrange_result2nd-UDGM-seperated/" 
# datapath = "C:/Users/Tada/Documents/Telecom_local/arrange_result_old/" 
# datapath = "C:/Users/Tada/Documents/Telecom_local/arrange_result_my-LFC-from-old/" 
# datapath = "C:/Users/Tada/Documents/Telecom_local/arrange_result_my-LFC-from-old/old_4/" 

outliner = []
# outliner = ['normal/100-60/1',
# 'normal/100-70/10',
# 'normal/100-80/2',
# 'normal/100-80/10',
# 'normal/100-90/3',
# 'normal/100-90/4',
# 'normal/100-100/6',
# 'normal/100-100/9',
# 'normal-re2/100-60/1',
# 'normal-re2/100-60/3',
# 'normal-re2/100-60/4',
# 'normal-re2/100-60/6',
# 'normal-re2/100-70/2',
# 'normal-re2/100-70/3',
# 'normal-re2/100-70/4',
# 'normal-re2/100-70/10',
# 'normal-re2/100-80/3',
# 'normal-re2/100-80/4',
# 'normal-re2/100-80/9',
# 'normal-re2/100-80/10',
# 'normal-re2/100-100/6',
# 'normal-re4/100-60/1',
# 'normal-re4/100-60/2',
# 'normal-re4/100-60/3',
# 'normal-re4/100-60/6',
# 'normal-re4/100-60/8',
# 'normal-re4/100-70/3',
# 'normal-re4/100-70/6',
# 'normal-re4/100-80/3',
# 'normal-re4/100-80/8',
# 'normal-re4/100-90/1',
# 'normal-re4/100-90/4',
# 'normal-re4/100-90/6',
# 'normal-re4/100-100/3',
# 'normal-re4/100-100/6',
# 'normal-re6/100-60/2',
# 'normal-re6/100-60/5',
# 'normal-re6/100-60/7',
# 'normal-re6/100-70/2',
# 'normal-re6/100-70/6',
# 'normal-re6/100-70/10',
# 'normal-re6/100-100/3',
# 'normal-re6/100-100/7',
# 'normal-re8/100-60/2',
# 'normal-re8/100-70/4',
# 'normal-re8/100-70/7',
# 'leapfrog/100-60/4',
# 'leapfrog/100-60/5',
# 'leapfrog/100-60/6',
# 'leapfrog/100-70/3',
# 'leapfrog/100-80/5',
# 'leapfrog/100-100/8',
# 'leapfrog/100-100/9'] #for arrange_result2nd-UDGM

#parameters for targt files
tx_max = 100
tx_min = 100
tx_step = 10
rx_max = 100
rx_min = 100
rx_step = 1
sim_cnt_max = 20
sim_cnt_min = 1

#--------------plot color and textures---------------
color_no = ['orange', '/']
color_re2 = ['red', '*']
color_re4 = ['magenta', 'o']
color_re6 = ['blue', 'O']
color_re8 = ['cyan', '.']
color_lf = ['green', '\\']

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
	efficiency_graph_array = [] #pdr/array

	for tx in range(tx_min, tx_max+1, tx_step):
		for rx in range(rx_min, rx_max+1, rx_step):
			print directory_name + "/" + str(tx) + "-" + str(rx)
			pdr_array = []
			send_array = []
			receive_array = []
			replication_array = []
			elimination_array = []
			nrg_net_total_array = []
			nrg_net_avg_array = []
			delay_array = []
			jitter_array = []
			efficiency_array = []
			#gather data for each different random seeds
			for sim_cnt in range(sim_cnt_min, sim_cnt_max+1):
				# print tx, "-", rx, "-", sim_cnt
				input_file_name = datapath + directory_name + "/" + str(tx) + "-" + str(rx) + "/" + str(sim_cnt) + "/" + "COOJA.testlog"
				for temp_outliner in outliner:
					if datapath + temp_outliner + "/COOJA.testlog" == input_file_name:
						break
				else:
					result = get_result_from_file(input_file_name)
				 	print "input:", directory_name + "/" + str(tx) + "-" + str(rx) + "/" + str(sim_cnt) + "/" + "COOJA.testlog",
					print "pdr:", "{0:.2f}".format(result[0]), "s:", result[1], "r:", result[2], "delay(ms):", "{0:.2f}".format(result[9]), "jitter(ms):", "{0:.2f}".format(result[10]),
					print "efficiency(%/s):", "{0:.5f}".format(result[11]),
					print "rep:", result[3], "eli:", result[4],
					pdr_array.append(result[0])
					send_array.append(result[1])
					receive_array.append(result[2])
					replication_array.append(result[3])
					elimination_array.append(result[4])
					nrg_net_total_array.append(result[5])
					nrg_net_avg_array.append(result[6])
					delay_array.append(result[9])
					jitter_array.append(result[10])
					efficiency_array.append(result[11])

					#for getting random seeds
					print "seed:", get_randomseed_from_file(datapath + directory_name + "/" + str(tx) + "-" + str(rx) + "/" + str(sim_cnt) + "/" + "COOJA.log")

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
			efficiency_graph_array.append(efficiency_array)

			print "Use", len(pdr_array), "file(s)"

	return [pdr_graph_array, send_graph_array, receive_graph_array, replication_graph_array, elimination_graph_array, \
	nrg_net_total_graph_array, nrg_net_avg_graph_array, \
	delay_graph_array, jitter_graph_array,\
	efficiency_graph_array]

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
efficiency_no = result[9]

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
efficiency_re2 = result[9]

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
efficiency_re4 = result[9]

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
efficiency_re6 = result[9]

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
efficiency_re8 = result[9]

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
efficiency_lf = result[9]

#--------------PDR boxplot-------------
fig, ax = plt.subplots()

for i in range(0, int(rx_max/10)-int(rx_min/10) + 1):
	bp = plt.boxplot(pdr_no[i], positions=[i], patch_artist=True)
	set_boxplot_color(bp, color_no[0], color_no[1])
	bp = plt.boxplot(pdr_re2[i], positions=[i], patch_artist=True)
	set_boxplot_color(bp, color_re2[0], color_re2[1])
	bp = plt.boxplot(pdr_re4[i], positions=[i], patch_artist=True)
	set_boxplot_color(bp, color_re4[0], color_re4[1])
	bp = plt.boxplot(pdr_re6[i], positions=[i], patch_artist=True)
	set_boxplot_color(bp, color_re6[0], color_re6[1])
	bp = plt.boxplot(pdr_re8[i], positions=[i], patch_artist=True)
	set_boxplot_color(bp, color_re8[0], color_re8[1])
	bp = plt.boxplot(pdr_lf[i], positions=[i], patch_artist=True)
	set_boxplot_color(bp, color_lf[0], color_lf[1])

#xticks
xticks = []
for i in range(rx_min/10, rx_max/10 + 1):
	xticks.append(str(i*10))
plt.xticks([i for i in range(0, len(xticks))], xticks, rotation=270) #must be changed correpoiding to the number of data

#only used for making legends
ax.bar([1], [0], color='white', edgecolor=color_no[0], hatch=color_no[1], label='default ReTx=0')
ax.bar([1], [0], color='white', edgecolor=color_re2[0], hatch=color_re2[1], label='default ReTx=2')
ax.bar([1], [0], color='white', edgecolor=color_re4[0], hatch=color_re4[1], label='default ReTx=4')
ax.bar([1], [0], color='white', edgecolor=color_re6[0], hatch=color_re6[1], label='default ReTx=6')
ax.bar([1], [0], color='white', edgecolor=color_re8[0], hatch=color_re8[1], label='default ReTx=8')
ax.bar([1], [0], color='white', edgecolor=color_lf[0], hatch=color_lf[1], label='Leapfrog Collaboration')
plt.legend(ncol=2, loc='lower right', fontsize=10)
ax.set_xlabel('Link quality (%)')
ax.set_ylabel('Packet Delivery Ratio')

fig.savefig(datapath + "pdr" + ".png")

#--------------Energy boxplot-------------
fig, ax = plt.subplots()

for i in range(0, int(rx_max/10)-int(rx_min/10) + 1):
	bp = plt.boxplot(nrg_net_avg_no[i], positions=[i], patch_artist=True)
	set_boxplot_color(bp, color_no[0], color_no[1])
	bp = plt.boxplot(nrg_net_avg_re2[i], positions=[i], patch_artist=True)
	set_boxplot_color(bp, color_re2[0], color_re2[1])
	bp = plt.boxplot(nrg_net_avg_re4[i], positions=[i], patch_artist=True)
	set_boxplot_color(bp, color_re4[0], color_re4[1])
	bp = plt.boxplot(nrg_net_avg_re6[i], positions=[i], patch_artist=True)
	set_boxplot_color(bp, color_re6[0], color_re6[1])
	bp = plt.boxplot(nrg_net_avg_re8[i], positions=[i], patch_artist=True)
	set_boxplot_color(bp, color_re8[0], color_re8[1])
	bp = plt.boxplot(nrg_net_avg_lf[i], positions=[i], patch_artist=True)
	set_boxplot_color(bp, color_lf[0], color_lf[1])

#xticks
xticks = []
for i in range(rx_min/10, rx_max/10 + 1):
	xticks.append(str(i*10))
plt.xticks([i for i in range(0, len(xticks))], xticks, rotation=270) #must be changed correpoiding to the number of data

#only used for making legends
ax.bar([1], [0], color='white', edgecolor=color_no[0], hatch=color_no[1], label='default ReTx=0')
ax.bar([1], [0], color='white', edgecolor=color_re2[0], hatch=color_re2[1], label='default ReTx=2')
ax.bar([1], [0], color='white', edgecolor=color_re4[0], hatch=color_re4[1], label='default ReTx=4')
ax.bar([1], [0], color='white', edgecolor=color_re6[0], hatch=color_re6[1], label='default ReTx=6')
ax.bar([1], [0], color='white', edgecolor=color_re8[0], hatch=color_re8[1], label='default ReTx=8')
ax.bar([1], [0], color='white', edgecolor=color_lf[0], hatch=color_lf[1], label='Leapfrog Collaboration')
plt.legend(ncol=2, loc='upper right', fontsize=10)
ax.set_xlabel('Link quality (%)')
ax.set_ylabel('Average energy consumption of nodes (mW)')
ax.set_ylim(6,10)

fig.savefig(datapath + "nrg" + ".png")

#--------------delay boxplot-------------
fig, ax = plt.subplots()

for i in range(0, int(rx_max/10)-int(rx_min/10) + 1):
	bp = plt.boxplot(delay_no[i], positions=[i], patch_artist=True)
	set_boxplot_color(bp, color_no[0], color_no[1])
	bp = plt.boxplot(delay_re2[i], positions=[i], patch_artist=True)
	set_boxplot_color(bp, color_re2[0], color_re2[1])
	bp = plt.boxplot(delay_re4[i], positions=[i], patch_artist=True)
	set_boxplot_color(bp, color_re4[0], color_re4[1])
	bp = plt.boxplot(delay_re6[i], positions=[i], patch_artist=True)
	set_boxplot_color(bp, color_re6[0], color_re6[1])
	bp = plt.boxplot(delay_re8[i], positions=[i], patch_artist=True)
	set_boxplot_color(bp, color_re8[0], color_re8[1])
	bp = plt.boxplot(delay_lf[i], positions=[i], patch_artist=True)
	set_boxplot_color(bp, color_lf[0], color_lf[1])

#xticks
xticks = []
for i in range(rx_min/10, rx_max/10 + 1):
	xticks.append(str(i*10))
plt.xticks([i for i in range(0, len(xticks))], xticks, rotation=270) #must be changed correpoiding to the number of data

#only used for making legends
ax.bar([1], [0], color='white', edgecolor=color_no[0], hatch=color_no[1], label='default ReTx=0')
ax.bar([1], [0], color='white', edgecolor=color_re2[0], hatch=color_re2[1], label='default ReTx=2')
ax.bar([1], [0], color='white', edgecolor=color_re4[0], hatch=color_re4[1], label='default ReTx=4')
ax.bar([1], [0], color='white', edgecolor=color_re6[0], hatch=color_re6[1], label='default ReTx=6')
ax.bar([1], [0], color='white', edgecolor=color_re8[0], hatch=color_re8[1], label='default ReTx=8')
ax.bar([1], [0], color='white', edgecolor=color_lf[0], hatch=color_lf[1], label='Leapfrog Collaboration')
plt.legend(ncol=2, loc='lower right', fontsize=10)
ax.set_xlabel('Link quality (%)')
ax.set_ylabel('Delay (ms)')
ax.set_ylim(0,10000)

fig.savefig(datapath + "delay" + ".png")

#--------------jitter boxplot-------------
fig, ax = plt.subplots()

for i in range(0, int(rx_max/10)-int(rx_min/10) + 1):
	bp = plt.boxplot(jitter_no[i], positions=[i], patch_artist=True)
	set_boxplot_color(bp, color_no[0], color_no[1])
	bp = plt.boxplot(jitter_re2[i], positions=[i], patch_artist=True)
	set_boxplot_color(bp, color_re2[0], color_re2[1])
	bp = plt.boxplot(jitter_re4[i], positions=[i], patch_artist=True)
	set_boxplot_color(bp, color_re4[0], color_re4[1])
	bp = plt.boxplot(jitter_re6[i], positions=[i], patch_artist=True)
	set_boxplot_color(bp, color_re6[0], color_re6[1])
	bp = plt.boxplot(jitter_re8[i], positions=[i], patch_artist=True)
	set_boxplot_color(bp, color_re8[0], color_re8[1])
	bp = plt.boxplot(jitter_lf[i], positions=[i], patch_artist=True)
	set_boxplot_color(bp, color_lf[0], color_lf[1])

#xticks
xticks = []
for i in range(rx_min/10, rx_max/10 + 1):
	xticks.append(str(i*10))
plt.xticks([i for i in range(0, len(xticks))], xticks, rotation=270) #must be changed correpoiding to the number of data

#only used for making legends
ax.bar([1], [0], color='white', edgecolor=color_no[0], hatch=color_no[1], label='default ReTx=0')
ax.bar([1], [0], color='white', edgecolor=color_re2[0], hatch=color_re2[1], label='default ReTx=2')
ax.bar([1], [0], color='white', edgecolor=color_re4[0], hatch=color_re4[1], label='default ReTx=4')
ax.bar([1], [0], color='white', edgecolor=color_re6[0], hatch=color_re6[1], label='default ReTx=6')
ax.bar([1], [0], color='white', edgecolor=color_re8[0], hatch=color_re8[1], label='default ReTx=8')
ax.bar([1], [0], color='white', edgecolor=color_lf[0], hatch=color_lf[1], label='Leapfrog Collaboration')
plt.legend(ncol=2, loc='lower right', fontsize=10)
ax.set_xlabel('Link quality (%)')
ax.set_ylabel('Jitter: packet interarrival time (ms)')
ax.set_ylim(50000, 200000)

fig.savefig(datapath + "jitter" + ".png")

#--------------efficiency boxplot-------------
fig, ax = plt.subplots()

for i in range(0, int(rx_max/10)-int(rx_min/10) + 1):
	bp = plt.boxplot(efficiency_no[i], positions=[i], patch_artist=True)
	set_boxplot_color(bp, color_no[0], color_no[1])
	bp = plt.boxplot(efficiency_re2[i], positions=[i], patch_artist=True)
	set_boxplot_color(bp, color_re2[0], color_re2[1])
	bp = plt.boxplot(efficiency_re4[i], positions=[i], patch_artist=True)
	set_boxplot_color(bp, color_re4[0], color_re4[1])
	bp = plt.boxplot(efficiency_re6[i], positions=[i], patch_artist=True)
	set_boxplot_color(bp, color_re6[0], color_re6[1])
	bp = plt.boxplot(efficiency_re8[i], positions=[i], patch_artist=True)
	set_boxplot_color(bp, color_re8[0], color_re8[1])
	bp = plt.boxplot(efficiency_lf[i], positions=[i], patch_artist=True)
	set_boxplot_color(bp, color_lf[0], color_lf[1])

#xticks
xticks = []
for i in range(rx_min/10, rx_max/10 + 1):
	xticks.append(str(i*10))
plt.xticks([i for i in range(0, len(xticks))], xticks, rotation=270) #must be changed correpoiding to the number of data

#only used for making legends
ax.bar([1], [0], color='white', edgecolor=color_no[0], hatch=color_no[1], label='default ReTx=0')
ax.bar([1], [0], color='white', edgecolor=color_re2[0], hatch=color_re2[1], label='default ReTx=2')
ax.bar([1], [0], color='white', edgecolor=color_re4[0], hatch=color_re4[1], label='default ReTx=4')
ax.bar([1], [0], color='white', edgecolor=color_re6[0], hatch=color_re6[1], label='default ReTx=6')
ax.bar([1], [0], color='white', edgecolor=color_re8[0], hatch=color_re8[1], label='default ReTx=8')
ax.bar([1], [0], color='white', edgecolor=color_lf[0], hatch=color_lf[1], label='Leapfrog Collaboration')
plt.legend(ncol=2, loc='lower right', fontsize=10)
ax.set_xlabel('Link quality (%)')
ax.set_ylabel('Efficiency (%/s)')

fig.savefig(datapath + "efficiency" + ".png")

#-------------------------------------------------------------
#-------------------------additional plots--------------------
#-------------------------------------------------------------

#------------------- PDR averge making average line graph
pdr_avg_no = []
pdr_avg_lf = []
pdr_avg_re2 = []
pdr_avg_re4 = []
pdr_avg_re6 = []
pdr_avg_re8 = []
pdr_error_no = []
pdr_error_lf = []
pdr_error_re2 = []
pdr_error_re4 = []
pdr_error_re6 = []
pdr_error_re8 = []
for i in range(0, int(rx_max/10)-int(rx_min/10) + 1):
	pdr_avg_no.append(np.average(pdr_no[i]))
	pdr_avg_lf.append(np.average(pdr_lf[i]))
	pdr_avg_re2.append(np.average(pdr_re2[i]))
	pdr_avg_re4.append(np.average(pdr_re4[i]))
	pdr_avg_re6.append(np.average(pdr_re6[i]))
	pdr_avg_re8.append(np.average(pdr_re8[i]))
	pdr_error_no.append(np.std(pdr_no[i]))
	pdr_error_lf.append(np.std(pdr_lf[i]))
	pdr_error_re2.append(np.std(pdr_re2[i]))
	pdr_error_re4.append(np.std(pdr_re4[i]))
	pdr_error_re6.append(np.std(pdr_re6[i]))
	pdr_error_re8.append(np.std(pdr_re8[i]))
fig = plt.figure()
ax = fig.add_subplot(111)
x = np.arange(rx_min, rx_max+1, 10)
ax.errorbar(x, pdr_avg_no, yerr=pdr_error_no, ecolor=color_no[0])
ax.errorbar(x, pdr_avg_re2, yerr=pdr_error_re2, ecolor=color_re2[0])
ax.errorbar(x, pdr_avg_re4, yerr=pdr_error_re4, ecolor=color_re4[0])
ax.errorbar(x, pdr_avg_re6, yerr=pdr_error_re6, ecolor=color_re6[0])
ax.errorbar(x, pdr_avg_re8, yerr=pdr_error_re8, ecolor=color_re8[0])
ax.errorbar(x, pdr_avg_lf, yerr=pdr_error_lf, ecolor=color_lf[0])
ax.plot(x, pdr_avg_no, 'o-', color=color_no[0], label="default ReTx=0")
ax.plot(x, pdr_avg_re2, '+-', color=color_re2[0], label="default ReTx=2")
ax.plot(x, pdr_avg_re4, '^-', color=color_re4[0], label="default ReTx=4")
ax.plot(x, pdr_avg_re6, 's-', color=color_re6[0], label="default ReTx=6")
ax.plot(x, pdr_avg_re8, 'D-', color=color_re8[0], label="default ReTx=8")
ax.plot(x, pdr_avg_lf, 'x-', color=color_lf[0], label="Leapfrog Collaboration")

ax.set_xlabel('Link quality (%)')
ax.set_ylabel('Packet Delivery Ratio (%)')
ax.legend(ncol=1, loc="upper left", fontsize=10)
fig.savefig(datapath + "pdr_line" + ".png")

#-----------------NRG averge making average line graph
nrg_net_avg_avg_no = []
nrg_net_avg_avg_lf = []
nrg_net_avg_avg_re2 = []
nrg_net_avg_avg_re4 = []
nrg_net_avg_avg_re6 = []
nrg_net_avg_avg_re8 = []
nrg_net_avg_error_no = []
nrg_net_avg_error_lf = []
nrg_net_avg_error_re2 = []
nrg_net_avg_error_re4 = []
nrg_net_avg_error_re6 = []
nrg_net_avg_error_re8 = []
for i in range(0, int(rx_max/10)-int(rx_min/10) + 1):
	nrg_net_avg_avg_no.append(np.average(nrg_net_avg_no[i]))
	nrg_net_avg_avg_lf.append(np.average(nrg_net_avg_lf[i]))
	nrg_net_avg_avg_re2.append(np.average(nrg_net_avg_re2[i]))
	nrg_net_avg_avg_re4.append(np.average(nrg_net_avg_re4[i]))
	nrg_net_avg_avg_re6.append(np.average(nrg_net_avg_re6[i]))
	nrg_net_avg_avg_re8.append(np.average(nrg_net_avg_re8[i]))

	nrg_net_avg_error_no.append(np.std(nrg_net_avg_no[i]))
	nrg_net_avg_error_lf.append(np.std(nrg_net_avg_lf[i]))
	nrg_net_avg_error_re2.append(np.std(nrg_net_avg_re2[i]))
	nrg_net_avg_error_re4.append(np.std(nrg_net_avg_re4[i]))
	nrg_net_avg_error_re6.append(np.std(nrg_net_avg_re6[i]))
	nrg_net_avg_error_re8.append(np.std(nrg_net_avg_re8[i]))

fig = plt.figure()
ax = fig.add_subplot(111)
x = np.arange(rx_min, rx_max+1, 10)
ax.errorbar(x, nrg_net_avg_avg_no, yerr=nrg_net_avg_error_no, ecolor=color_no[0])
ax.errorbar(x, nrg_net_avg_avg_re2, yerr=nrg_net_avg_error_re2, ecolor=color_re2[0])
ax.errorbar(x, nrg_net_avg_avg_re4, yerr=nrg_net_avg_error_re4, ecolor=color_re4[0])
ax.errorbar(x, nrg_net_avg_avg_re6, yerr=nrg_net_avg_error_re6, ecolor=color_re6[0])
ax.errorbar(x, nrg_net_avg_avg_re8, yerr=nrg_net_avg_error_re8, ecolor=color_re8[0])
ax.errorbar(x, nrg_net_avg_avg_lf, yerr=nrg_net_avg_error_lf, ecolor=color_lf[0])
ax.plot(x, nrg_net_avg_avg_no, 'o-', color=color_no[0], label="default ReTx=0")
ax.plot(x, nrg_net_avg_avg_re2, '+-', color=color_re2[0], label="default ReTx=2")
ax.plot(x, nrg_net_avg_avg_re4, '^-', color=color_re4[0], label="default ReTx=4")
ax.plot(x, nrg_net_avg_avg_re6, 's-', color=color_re6[0], label="default ReTx=6")
ax.plot(x, nrg_net_avg_avg_re8, 'D-', color=color_re8[0], label="default ReTx=8")
ax.plot(x, nrg_net_avg_avg_lf, 'x-', color=color_lf[0], label="Leapfrog Collaboration")
ax.set_xlabel('Link quality (%)')
ax.set_ylabel('Average energy consumption of nodes (mW)')
ax.legend(ncol=1, loc="upper right", fontsize=10)
fig.savefig(datapath + "nrg_line" + ".png")

#------------------- Delay averge making average line graph
delay_avg_no = []
delay_avg_lf = []
delay_avg_re2 = []
delay_avg_re4 = []
delay_avg_re6 = []
delay_avg_re8 = []
delay_error_no = []
delay_error_lf = []
delay_error_re2 = []
delay_error_re4 = []
delay_error_re6 = []
delay_error_re8 = []
for i in range(0, int(rx_max/10)-int(rx_min/10) + 1):
	delay_avg_no.append(np.average(delay_no[i]))
	delay_avg_lf.append(np.average(delay_lf[i]))
	delay_avg_re2.append(np.average(delay_re2[i]))
	delay_avg_re4.append(np.average(delay_re4[i]))
	delay_avg_re6.append(np.average(delay_re6[i]))
	delay_avg_re8.append(np.average(delay_re8[i]))
	delay_error_no.append(np.std(delay_no[i]))
	delay_error_lf.append(np.std(delay_lf[i]))
	delay_error_re2.append(np.std(delay_re2[i]))
	delay_error_re4.append(np.std(delay_re4[i]))
	delay_error_re6.append(np.std(delay_re6[i]))
	delay_error_re8.append(np.std(delay_re8[i]))
fig = plt.figure()
ax = fig.add_subplot(111)
x = np.arange(rx_min, rx_max+1, 10)
ax.errorbar(x, delay_avg_no, yerr=delay_error_no, ecolor=color_no[0])
ax.errorbar(x, delay_avg_re2, yerr=delay_error_re2, ecolor=color_re2[0])
ax.errorbar(x, delay_avg_re4, yerr=delay_error_re4, ecolor=color_re4[0])
ax.errorbar(x, delay_avg_re6, yerr=delay_error_re6, ecolor=color_re6[0])
ax.errorbar(x, delay_avg_re8, yerr=delay_error_re8, ecolor=color_re8[0])
ax.errorbar(x, delay_avg_lf, yerr=delay_error_lf, ecolor=color_lf[0])
ax.plot(x, delay_avg_no, 'o-', color=color_no[0], label="default ReTx=0")
ax.plot(x, delay_avg_re2, '+-', color=color_re2[0], label="default ReTx=2")
ax.plot(x, delay_avg_re4, '^-', color=color_re4[0], label="default ReTx=4")
ax.plot(x, delay_avg_re6, 's-', color=color_re6[0], label="default ReTx=6")
ax.plot(x, delay_avg_re8, 'D-', color=color_re8[0], label="default ReTx=8")
ax.plot(x, delay_avg_lf, 'x-', color=color_lf[0], label="Leapfrog Collaboration")

ax.set_xlabel('Link quality (%)')
ax.set_ylabel('Delay (ms)')
ax.legend(ncol=1, loc="upper left", fontsize=10)
fig.savefig(datapath + "delay_line" + ".png")

#------------------- jitter averge making average line graph
jitter_avg_no = []
jitter_avg_lf = []
jitter_avg_re2 = []
jitter_avg_re4 = []
jitter_avg_re6 = []
jitter_avg_re8 = []
jitter_error_no = []
jitter_error_lf = []
jitter_error_re2 = []
jitter_error_re4 = []
jitter_error_re6 = []
jitter_error_re8 = []
for i in range(0, int(rx_max/10)-int(rx_min/10) + 1):
	jitter_avg_no.append(np.average(jitter_no[i]))
	jitter_avg_lf.append(np.average(jitter_lf[i]))
	jitter_avg_re2.append(np.average(jitter_re2[i]))
	jitter_avg_re4.append(np.average(jitter_re4[i]))
	jitter_avg_re6.append(np.average(jitter_re6[i]))
	jitter_avg_re8.append(np.average(jitter_re8[i]))
	jitter_error_no.append(np.std(jitter_no[i]))
	jitter_error_lf.append(np.std(jitter_lf[i]))
	jitter_error_re2.append(np.std(jitter_re2[i]))
	jitter_error_re4.append(np.std(jitter_re4[i]))
	jitter_error_re6.append(np.std(jitter_re6[i]))
	jitter_error_re8.append(np.std(jitter_re8[i]))
fig = plt.figure()
ax = fig.add_subplot(111)
x = np.arange(rx_min, rx_max+1, 10)
ax.errorbar(x, jitter_avg_no, yerr=jitter_error_no, ecolor=color_no[0])
ax.errorbar(x, jitter_avg_re2, yerr=jitter_error_re2, ecolor=color_re2[0])
ax.errorbar(x, jitter_avg_re4, yerr=jitter_error_re4, ecolor=color_re4[0])
ax.errorbar(x, jitter_avg_re6, yerr=jitter_error_re6, ecolor=color_re6[0])
ax.errorbar(x, jitter_avg_re8, yerr=jitter_error_re8, ecolor=color_re8[0])
ax.errorbar(x, jitter_avg_lf, yerr=jitter_error_lf, ecolor=color_lf[0])
ax.plot(x, jitter_avg_no, 'o-', color=color_no[0], label="default ReTx=0")
ax.plot(x, jitter_avg_re2, '+-', color=color_re2[0], label="default ReTx=2")
ax.plot(x, jitter_avg_re4, '^-', color=color_re4[0], label="default ReTx=4")
ax.plot(x, jitter_avg_re6, 's-', color=color_re6[0], label="default ReTx=6")
ax.plot(x, jitter_avg_re8, 'D-', color=color_re8[0], label="default ReTx=8")
ax.plot(x, jitter_avg_lf, 'x-', color=color_lf[0], label="Leapfrog Collaboration")

ax.set_xlabel('Link quality (%)')
ax.set_ylabel('Jitter: packet interarrival time (ms)')
ax.legend(ncol=1, loc="upper left", fontsize=10)
fig.savefig(datapath + "jitter_line" + ".png")

#------------------- efficiency averge making average line graph
efficiency_avg_no = []
efficiency_avg_lf = []
efficiency_avg_re2 = []
efficiency_avg_re4 = []
efficiency_avg_re6 = []
efficiency_avg_re8 = []
efficiency_error_no = []
efficiency_error_lf = []
efficiency_error_re2 = []
efficiency_error_re4 = []
efficiency_error_re6 = []
efficiency_error_re8 = []
for i in range(0, int(rx_max/10)-int(rx_min/10) + 1):
	efficiency_avg_no.append(np.average(efficiency_no[i]))
	efficiency_avg_lf.append(np.average(efficiency_lf[i]))
	efficiency_avg_re2.append(np.average(efficiency_re2[i]))
	efficiency_avg_re4.append(np.average(efficiency_re4[i]))
	efficiency_avg_re6.append(np.average(efficiency_re6[i]))
	efficiency_avg_re8.append(np.average(efficiency_re8[i]))
	efficiency_error_no.append(np.std(efficiency_no[i]))
	efficiency_error_lf.append(np.std(efficiency_lf[i]))
	efficiency_error_re2.append(np.std(efficiency_re2[i]))
	efficiency_error_re4.append(np.std(efficiency_re4[i]))
	efficiency_error_re6.append(np.std(efficiency_re6[i]))
	efficiency_error_re8.append(np.std(efficiency_re8[i]))
fig = plt.figure()
ax = fig.add_subplot(111)
x = np.arange(rx_min, rx_max+1, 10)
ax.errorbar(x, efficiency_avg_no, yerr=efficiency_error_no, ecolor=color_no[0])
ax.errorbar(x, efficiency_avg_re2, yerr=efficiency_error_re2, ecolor=color_re2[0])
ax.errorbar(x, efficiency_avg_re4, yerr=efficiency_error_re4, ecolor=color_re4[0])
ax.errorbar(x, efficiency_avg_re6, yerr=efficiency_error_re6, ecolor=color_re6[0])
ax.errorbar(x, efficiency_avg_re8, yerr=efficiency_error_re8, ecolor=color_re8[0])
ax.errorbar(x, efficiency_avg_lf, yerr=efficiency_error_lf, ecolor=color_lf[0])
ax.plot(x, efficiency_avg_no, 'o-', color=color_no[0], label="default ReTx=0")
ax.plot(x, efficiency_avg_re2, '+-', color=color_re2[0], label="default ReTx=2")
ax.plot(x, efficiency_avg_re4, '^-', color=color_re4[0], label="default ReTx=4")
ax.plot(x, efficiency_avg_re6, 's-', color=color_re6[0], label="default ReTx=6")
ax.plot(x, efficiency_avg_re8, 'D-', color=color_re8[0], label="default ReTx=8")
ax.plot(x, efficiency_avg_lf, 'x-', color=color_lf[0], label="Leapfrog Collaboration")

ax.set_xlabel('Link quality (%)')
ax.set_ylabel('Efficiency (%/s)')
ax.legend(ncol=1, loc="upper left", fontsize=10)
fig.savefig(datapath + "efficiency_line" + ".png")

#---------------fin and show -------------
print "finish to draw figures. Plase look at ", datapath
print "finish to draw figures. Plase look at ", datapath
print "finish to draw figures. Plase look at ", datapath
# plt.show()