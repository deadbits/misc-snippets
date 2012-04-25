#!/usr/bin/python

import httplib
import sys
import argparse

help = """Checks if a given website is active or not"""

parser = argparse.ArgumentParser(description=help)
parser.add_argument("--www", help="website", required=True)
parser.add_argument("--port", help="port", type=int, default=80)
args = parser.parse_args()

hostname = args.www
port = args.port

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
