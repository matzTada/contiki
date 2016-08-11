import sys
from xml.dom import minidom

params = sys.argv
xmlfile = "test.csc"
next_tx = 1.0
next_rx = 1.0

pdrfile = "test.csv"
LINK_ARRAY = \
['1-2', '1-3', '2-3', '2-4', '3-5', \
'2-5', '3-4', '4-5', '4-6', '5-7', \
'4-7', '5-6', '6-7', '6-8', '7-8']
# PDR_ARRAY = [94 , 94 , 85 , 41 , 99 , 99 , 87 , 86 , 10 , 100 , 9 , 89 , 92 , 97 , 83 , ]
PDR_ARRAY = []
run_id = 0

#command paramter processing
try:
	xmlfile = params[1]
	pdrfile = params[2]
	run_id = int(params[3])
	# next_tx = float(params[2]) / 100
	# next_rx = float(params[3]) / 100
	print "Try to change xmlfile:", xmlfile
	print "with using pdrfile:", pdrfile
	print "run_id", run_id
	# print "Change next param tx:", next_tx, "rx:", next_rx
except:
	print "Argument error. exit"
	exit()

#prepare PDR_ARRAY from pdrfile
try:
	input_pdr_file = open(pdrfile)
	for line in input_pdr_file:
		items = line.split(",")
		if (len(items) > len(LINK_ARRAY) + 1) and (int(items[0].split(":")[1]) == run_id):
			print "Find data!!"
			for i in range(1, len(LINK_ARRAY) + 1):
				PDR_ARRAY.append(int(items[i]))
			break		
	else:
		print "Cannot find data. exit"
		input_pdr_file.close()
		exit()
	input_pdr_file.close()
except:
	print "Cannot find file:", pdrfile, ". exit"
	input_pdr_file.close()
	exit()

#making matrix with LINK_ARRAY and PDR_ARRAY
# Creates a list containing 5 lists, each of 8 items, all set to 0 w, h = 8, 5.  Matrix = [[0 for x in range(w)] for y in range(h)] 
adjancency_pdr_matrix = [[0 for x in range(0, len(LINK_ARRAY))] for y in range(0, len(LINK_ARRAY))]
for i in range(0, len(LINK_ARRAY)):
	#get coordinate from array
	x = int(LINK_ARRAY[i].split('-')[0]) - 1
	y = int(LINK_ARRAY[i].split('-')[1]) - 1
	adjancency_pdr_matrix[x][y] = PDR_ARRAY[i]
	adjancency_pdr_matrix[y][x] = PDR_ARRAY[i]

print "adjancency_pdr_matrix"
for i in range(0, len(LINK_ARRAY)):
	for j in range(0, len(LINK_ARRAY)):
		print adjancency_pdr_matrix[i][j],
	print ""

try:
	xdoc = minidom.parse(xmlfile)
except:
	print "Cannot find file:", xmlfile, ". exit"
	exit()

#print(xdoc.toxml()) #show all in the file

for e in xdoc.getElementsByTagName('edge'):
	# print "before",
	ele_src = e.getElementsByTagName('source')[0]
	src_id =  int(ele_src.childNodes[0].data)
	print 'src:', src_id,

	ele_dst_id = e.getElementsByTagName('radio')[0]
	dst_id = int(ele_dst_id.childNodes[0].data)
	print 'dst:', dst_id,

	ele_dst_ratio = e.getElementsByTagName('ratio')[0]
	print 'ratio:', ele_dst_ratio.childNodes[0].data,

	print "-->",
	next_rx = float(adjancency_pdr_matrix[src_id - 1][dst_id - 1]) / 100
	ele_dst_ratio.childNodes[0].data = next_rx
	print 'ratio:', ele_dst_ratio.childNodes[0].data

try:
	output = open(xmlfile, 'w')
	output.write(xdoc.toxml())
	print "File re-write succeed"
except:
	print "File write error. exit"
finally:
	output.close()

