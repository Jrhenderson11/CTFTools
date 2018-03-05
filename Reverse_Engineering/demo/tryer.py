import os
import sys

name = "./vuln-chat"
if (len(sys.argv) > 1):
	name = "./" + sys.argv[1]


for i in range(150):
	os.system("python exploit.py " + str(i) + "| " + name)