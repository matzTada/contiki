#!/bin/python
# script for extracing and preparing data from Berkley http://wsn.eecs.berkeley.edu/connectivity/download.php?dataset=soda
# extract PDR data randomly and save it to file

import numpy as np

INPUT_FILE_NAME = "soda_pdr.sql"
OUTPUT_FILE_NAME = "pdr_for_simulation.csv"
NUMBER_OF_LINK = 15

input_file = open(INPUT_FILE_NAME)

run_id = 1
array = []
save_str = ""

try:
	for line in input_file:
		items = line.split(",")
		# print "#", len(items),
		if len(items) == 6:
			if int(items[0].strip(' )(')) == run_id:
				# print int(items[4].strip(' )('))
				array.append(int(items[4].strip(' )(')))
			else:
				if len(array) >= NUMBER_OF_LINK:
					print "run_id:", run_id
					save_str += "id:" + str(run_id) + ","
					randomized_array = np.random.choice(array,  NUMBER_OF_LINK)
					print "randomized array:",
					for i in range(0, len(randomized_array)):
						print randomized_array[i], ",", 
						save_str += str(randomized_array[i]) + ","
					print ""
					save_str += "\n"
					run_id += 1
					array = [] #initialize
				else:
					break

	print save_str
	output_file = open(OUTPUT_FILE_NAME, "w")
	print "succeed in write file"
	output_file.write(save_str)

finally:
	input_file.close()
	output_file.close()

