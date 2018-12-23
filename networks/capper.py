from __future__ import print_function
import pyshark

cap = pyshark.FileCapture('Downloads/arp.pcap')
#print (cap[1].field_names)
#print cap[0]

MAC = '01:23:45:67:ab:cd'

right = False
for packet in cap:

	#src = packet['eth'].src
	#dst = packet['eth'].dst
	#packet.protocol

	if "ARP" in packet:
		if (packet['eth'].src==MAC):
			#print ("ARP " + packet['eth'].src)
			right = True
		else:
			right = False
	if not ("ARP" in packet) and "Data" in packet:
		if right:
			print ((packet.data.Data), end='')
	#x=raw_input()