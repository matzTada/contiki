#changing scenario.js and scenario.realsimfile 

import sys
from xml.dom import minidom

param = sys.argv
xmlfile = ""
next_scenario = ""
try:
	xmlfile = param[1]
	next_scenario = param[2]

	print "Try to change xmlfile:", xmlfile
	print "Change next param scenario:", next_scenario
except:
	print "Arguments error. exit"
	exit()

#for testing purpose
# xmlfile = "TEST.csc"
# next_scenario = "TEST_SCENARIO"

try:
	xdoc = minidom.parse(xmlfile)
except:
	print "Cannot find file:", xmlfile, ". exit"
	exit()

#print(xdoc.toxml()) #show all in the file

#for script.js for ScriptRunner
scriptfile_elements = xdoc.getElementsByTagName("scriptfile")[0]
print "scriptfile_elements bfr:", scriptfile_elements.childNodes[0].data
next_scriptfile = "[CONTIKI_DIR]/examples/ipv6/my-LFC-from-old/scenario/realsim/" + next_scenario + ".js"
scriptfile_elements.childNodes[0].data = next_scriptfile
print "scriptfile_elements aft:", scriptfile_elements.childNodes[0].data

#for Filename of RealsimFile
filename_elements = xdoc.getElementsByTagName("Filename")[0]
print "filename_elements bfr:", filename_elements.childNodes[0].data
next_filename = "[CONTIKI_DIR]/examples/ipv6/my-LFC-from-old/scenario/realsim/" + next_scenario + ".realsimfile"
filename_elements.childNodes[0].data = next_filename
print "filename_elements aft:", filename_elements.childNodes[0].data

try:
	output = open(xmlfile, "w")
	output.write(xdoc.toxml())
	print "File re-write succeed"
except:
	print "File write error. exit"
finally:
	output.close()
