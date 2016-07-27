import sys
from xml.dom import minidom

params = sys.argv
xmlfile = ""
next_tx = 1.0
next_rx = 1.0

try:
	xmlfile = params[1]
	next_tx = float(params[2]) / 100
	next_rx = float(params[3]) / 100
	print "Try to change xmlfile:", xmlfile
	print "Change next param tx:", next_tx, "rx:", next_rx
except:
	print "Argument error. exit"
	exit()

try:
	xdoc = minidom.parse(xmlfile)
except:
	print "Cannot find file:", xmlfile, ". exit"
	exit()

#print(xdoc.toxml()) #show all in the file

for e in xdoc.getElementsByTagName('edge'):
	print "before"
	ele_src = e.getElementsByTagName('source')[0]
	print 'src:', ele_src.childNodes[0].data,
	ele_dst_id = e.getElementsByTagName('radio')[0]
	print 'dst:', ele_dst_id.childNodes[0].data,
	ele_dst_ratio = e.getElementsByTagName('ratio')[0]
	print 'ratio:', ele_dst_ratio.childNodes[0].data

	print "after"
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

