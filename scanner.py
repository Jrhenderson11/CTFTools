import sys
from datetime import datetime
from scapy.all import *

def arp_scan():
	interface = "wlp4s0"
	ips = "192.168.0.0-25"

	start = datetime.now()
	print "starting scan"

	conf.verb=0

	ans,uans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst = ips), timeout=2, iface = interface, inter=0.1)

	for snd,rcv in ans:
		print rcv.sprintf(r"%Ether.src% - %ARP.psrc%")
	stop = datetime.now()
	print stop
	print stop-start