import os
import sys

name = "./vuln-chat"
if (len(sys.argv) > 1):
	name = "./" + sys.argv[1]

#segfault starts @ 25
for i in range(150):
	print i
	os.system("python exploit.py " + str(i) + "| " + name)
	print "-------------------------------------\n"