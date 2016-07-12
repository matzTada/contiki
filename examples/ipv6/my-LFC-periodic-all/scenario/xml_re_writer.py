import sys
from xml.dom import minidom

param = sys.argv
xmlfile = ""
next_tx = 1.0
next_rx = 1.0
try:
	xmlfile = param[1]
	next_tx = float(param[2]) / 100 
	next_rx = float(param[3]) / 100
	print "Try to change xmlfile:", xmlfile
	print "Change next param tx:", next_tx, "rx:", next_rx
except:
	print "Arguments error. exit"
	exit()

try:
	xdoc = minidom.parse(xmlfile)
except:
	print "Cannot find file:", xmlfile, ". exit"
	exit()

#print(xdoc.toxml()) #show all in the file

tx_ratio_elements = xdoc.getElementsByTagName("success_ratio_tx")[0]
rx_ratio_elements = xdoc.getElementsByTagName("success_ratio_rx")[0]

print "tx_ratio_elements before:", tx_ratio_elements.childNodes[0].data
print "rx_ratio_elements before:", rx_ratio_elements.childNodes[0].data

tx_ratio_elements.childNodes[0].data = next_tx
rx_ratio_elements.childNodes[0].data = next_rx

print "tx_ratio_elements after:", tx_ratio_elements.childNodes[0].data
print "rx_ratio_elements after:", rx_ratio_elements.childNodes[0].data

try:
	output = open(xmlfile, "w")
	output.write(xdoc.toxml())
	print "File re-write succeed"
except:
	print "File write error. exit"
finally:
	output.close()
