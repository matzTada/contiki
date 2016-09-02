from xml.dom import minidom
import matplotlib
import matplotlib.pyplot as plt

xmlfile = "test.csc"

#xml file specially csc
try:
	xdoc = minidom.parse(xmlfile)
except:
	print "Cannot find file:", xmlfile, ". exit"
	exit()

node_array = []
e_sim = xdoc.getElementsByTagName('simulation')[0]
for e in e_sim.getElementsByTagName('mote'):
	ele_id = e.getElementsByTagName('id')[0]
	nodeid = int(ele_id.childNodes[0].data)
	print 'id:', nodeid, 

	ele_x = e.getElementsByTagName('x')[0]
	x =  float(ele_x.childNodes[0].data)
	print 'x:', x,

	ele_y = e.getElementsByTagName('y')[0]
	y =  float(ele_x.childNodes[0].data)
	print 'y:', y,	
	print ""

	node_array.append([nodeid, x, y])