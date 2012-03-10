#!/usr/bin/python

import httplib
import sys

if len(sys.argv) < 3:
    print(".:: Simple HTTP Connection Checker ::.")
    print(" Usage: ./webcheck.py <hostname> <port>\n")
    sys.exit()

hostname = sys.argv[1]
port = sys.argv[2]

client = httplib.HTTPConnection(hostname,port)
client.request("GET","/")
response = client.getresponse()
client.close()

if response.status == 200:
    print("[+] Host: " + hostname + " is alive!\n")
    sys.exit()
if not response.status == 200:
    print("[!] Host: " + hostname + " might be down!\n[!] Response Code: " + response.reason)
    sys.exit()
    if response.reason == "Unauthorized":
        print("[!] You are not authorized to access this web-server!")
        sys.exit()
