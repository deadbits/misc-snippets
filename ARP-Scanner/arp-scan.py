#!/usr/bin/python

import string
import urllib2
from scapy.all import *

def NetworkMap():

    externalIP = ip = urllib2.urlopen("http://whatismyip.org").read()
    localIP = [x[4] for x in scapy.all.conf.route.routes if x[2] != '0.0.0.0'][0]
    splitIP = localIP.split('.')
    splitIP[3:] = (['0/24'])
    IPRange = '.'.join(splitIP)
    print("Local IP Address: " + localIP)
    print("Local IP Range: " + IPRange)
    print("External IP Addr: " + externalIP)
    print("\n[+] Searching for live hosts.....")
    conf.verb=0
    ans,unans=srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=IPRange),timeout=2)
    for snd,rcv in ans:
        mac_address=rcv.sprintf("%Ether.src%")
        ip_address=rcv.sprintf("%ARP.psrc%")
        print rcv.sprintf("\n\n[+] Host Found!\nMAC %Ether.src%\nIP: %ARP.psrc%\n ")

NetworkMap()

