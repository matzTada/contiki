#making Cumulative Distributed Function for link data for DGRM

import numpy as np
import matplotlib.pyplot as plt

input_file_name = "pdr_for_simulation.csv"

input_file = open(input_file_name)
input_lines = input_file.readlines()
input_file.close

# #for each
# for line in input_lines:
# 	fig, ax = plt.subplots()

# 	temp = line.split(',')
# 	dataid = int(temp[0].split(':')[1])
# 	num_data = len(temp) - 2

# 	y = []
# 	x = [i for i in range(0,101)]
# 	for tempx in x:
# 		percent = 0.0
# 		for i in range(1, num_data + 1):
# 			if int(temp[i]) < tempx:
# 				percent += 1
# 		y.append(percent)

# 	ax.plot(y, x)

# 	ax.set_ylabel('Link quality (%)')
# 	ax.set_xlabel('how many links are under the link quality')
# 	ax.set_xlim(0, num_data)

# 	fig.savefig("dataset" + str(dataid) + ".png")

#  	print dataid, num_data

#all in one
fig, ax = plt.subplots()
for line in input_lines:
	temp = line.split(',')
	dataid = int(temp[0].split(':')[1])
	num_data = len(temp) - 2

	y = []
	x = [i for i in range(0,101)]
	for tempx in x:
		percent = 0.0
		for i in range(1, num_data + 1):
			if int(temp[i]) < tempx:
				percent += 1
		y.append(percent)

	ax.plot(y, x)

ax.set_ylabel('Link quality (%)')
ax.set_xlabel('how many links are under the link quality')
ax.set_xlim(0, num_data)

fig.savefig("dataset" + "all" + ".png")
print "finish"
