import sys
from xml.dom import minidom

param = sys.argv
xmlfile = ""
next_seed = 1
try:
	xmlfile = param[1]
	next_seed = int(param[2]) 
	print "Try to change xmlfile:", xmlfile
	print "Change next param seed:", next_seed
except:
	print "Arguments error. exit"
	exit()

try:
	xdoc = minidom.parse(xmlfile)
except:
	print "Cannot find file:", xmlfile, ". exit"
	exit()

#print(xdoc.toxml()) #show all in the file

seed_elements = xdoc.getElementsByTagName("randomseed")[0]

print "seed_elements before:", seed_elements.childNodes[0].data

seed_elements.childNodes[0].data = next_seed

print "seed_elements after:", seed_elements.childNodes[0].data

try:
	output = open(xmlfile, "w")
	output.write(xdoc.toxml())
	print "File re-write succeed"
except:
	print "File write error. exit"
finally:
	output.close()
