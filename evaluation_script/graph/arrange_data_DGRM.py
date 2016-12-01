#python script file for extracting data from Cooja simulation result
#put this file in the same directory where "leapfrog" "normal" etc... exist
#This script is for the result with DGRM configuration as a radio medium

import numpy as np
import matplotlib.pyplot as plt
import csv

from mod_getdata import get_result_from_file ,set_boxplot_color

#data path
# datapath = "C:/Users/Tada/Documents/Telecom_local/arrange_result2nd-overhear-dgrm/" #for windows
#datapath = "C:/Users/Tada/Documents/Telecom_local/arrange_result2nd-overhear-dgrm-2/" #for windows
# datapath = "C:/Users/Tada/Documents/Telecom_local/arrange_result2nd-overhear-dgrm-3/" #for windows
# datapath = "C:/Users/Tada/Documents/Telecom_local/arrange_result2nd-overhear-dgrm-4/" #for windows
# datapath = "C:/Users/Tada/Documents/Telecom_local/arrange_result2nd-DGRM/" #for windows
datapath = "C:/Users/Tada/Documents/Telecom_local/arrange_result2nd-DGRM-seperated/" #for windows
# datapath = "C:/Users/Tada/Documents/Telecom_local/arrange_result-DGRM-check/" #for windows
# datapath = "C:/Users/Tada/Documents/Telecom_local/arrange_result-DGRM-perfect-seperated/" #for windows

#parameters for targt files
sim_cnt_max = 20
sim_cnt_min = 1

#--------------plot color and textures---------------
color_no = ['orange', '/']
color_re2 = ['red', '*']
color_re4 = ['magenta', 'o']
color_re6 = ['blue', 'O']
color_re8 = ['cyan', '.']
color_lf = ['green', '\\']

def get_graph_array_from_data(directory_name): #for DGRM
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
		print sim_cnt
		input_file_name = datapath + directory_name + "/" + str(sim_cnt) + "/" + "COOJA.testlog"
		result = get_result_from_file(input_file_name)
		pdr_array.append(result[0])
		send_array.append(result[1])
		receive_array.append(result[2])
		replication_array.append(result[3])
		elimination_array.append(result[4])
		nrg_net_total_array.append(result[5])
		nrg_net_avg_array.append(result[6])
		if result[9] !=0: #if delay = 0, it should not be added 
			delay_array.append(result[9])
		if result[10] != 0: #if jitter = 0, it should not be added
			jitter_array.append(result[10])
		if result[11] != 0:
			efficiency_array.append(result[11])

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

i = 0 # for i in range(10):
xticks = []
xticks.append('')

xticks.append('re0')
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

plt.legend(ncol=2, loc='lower left', fontsize=10)
ax.set_xlabel('Applied Algorithm Scheme')
ax.set_ylabel('Packet Delivery Ratio')

fig.savefig(datapath + "pdr" + ".png")

#--------------Energy boxplot-------------
fig, ax = plt.subplots()

i = 0 # for i in range(10):
xticks = []
xticks.append('')

xticks.append('re0')
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

plt.legend(ncol=2, loc='upper left', fontsize=10)
ax.set_xlabel('Applied Algorithm Scheme')
ax.set_ylabel('Average energy consumption of nodes (mW)')
ax.set_ylim(6, 9)

fig.savefig(datapath + "nrg" + ".png")

#--------------delay boxplot-------------
fig, ax = plt.subplots()

i = 0 # for i in range(10):
xticks = []
xticks.append('')

xticks.append('re0')
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

plt.legend(ncol=2, loc='lower left', fontsize=10)
ax.set_xlabel('Applied Algorithm Scheme')
ax.set_ylabel('Delay (ms)')
ax.set_ylim(0, 15000)

fig.savefig(datapath + "delay" + ".png")

#--------------jitter boxplot-------------
fig, ax = plt.subplots()

i = 0 # for i in range(10):
xticks = []
xticks.append('')

xticks.append('re0')
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

plt.legend(ncol=2, loc='upper right', fontsize=10)
ax.set_xlabel('Applied Algorithm Scheme')
ax.set_ylabel('Jitter: packet interarrival time (ms)')
ax.set_ylim(80000, 140000)

fig.savefig(datapath + "jitter" + ".png")

#--------------efficiency boxplot-------------
fig, ax = plt.subplots()

i = 0 # for i in range(10):
xticks = []
xticks.append('')

xticks.append('re0')
bp = plt.boxplot(efficiency_no[i], positions=[i + len(xticks)-1], patch_artist=True)
set_boxplot_color(bp, color_no[0], color_no[1])
xticks.append('re2')
bp = plt.boxplot(efficiency_re2[i], positions=[i + len(xticks)-1], patch_artist=True)
set_boxplot_color(bp, color_re2[0], color_re2[1])
xticks.append('re4')
bp = plt.boxplot(efficiency_re4[i], positions=[i + len(xticks)-1], patch_artist=True)
set_boxplot_color(bp, color_re4[0], color_re4[1])
xticks.append('re6')
bp = plt.boxplot(efficiency_re6[i], positions=[i + len(xticks)-1], patch_artist=True)
set_boxplot_color(bp, color_re6[0], color_re6[1])
xticks.append('re8')
bp = plt.boxplot(efficiency_re8[i], positions=[i + len(xticks)-1], patch_artist=True)
set_boxplot_color(bp, color_re8[0], color_re8[1])
xticks.append('lf')
bp = plt.boxplot(efficiency_lf[i], positions=[i + len(xticks)-1], patch_artist=True)
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

plt.legend(ncol=2, loc='upper left', fontsize=10)
ax.set_xlabel('Applied Algorithm Scheme')
ax.set_ylabel('Efficienty=pdr/delay_avg(%/s)')
# ax.set_ylim(80000, 140000)

fig.savefig(datapath + "efficiency" + ".png")

#---------------fin and show -------------
print "finish to draw figures. Plase look at ", datapath
print "finish to draw figures. Plase look at ", datapath
print "finish to draw figures. Plase look at ", datapath
# plt.show()