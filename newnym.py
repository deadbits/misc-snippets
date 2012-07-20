#!/usr/bin/python

# Get new TOR Identity

import telnetlib
import time, argparse

def newnym(host, port, pw):
    tn = telnetlib.Telnet(host, port)
    tn.write(('AUTHENTICATE "%s"\r\n' % pw ))
    res = tn.read_until('250 OK', 5)
    if res.find('250 OK') > -1:
       print('AUTHENICATE accepted.')
    tn.write("signal NEWNYM\r\n")
    res = tn.read_until('250 OK', 5)
    if res.find('250 OK') > -1:
       print("[+] New identity successfull")

def main():
    while True:
        newnym(host, port, pw)
        time.sleep(90)
        print("[+] New identity in 90 seconds...")
    

help = """Utilizes telnetlib to change TOR identities"""

parser = argparse.ArgumentParser(description=help)
parser.add_argument("--host", help="hostname, usually localhost", default="localhost")
parser.add_argument("--port", help="TOR control port", type=int, default=9051)
parser.add_argument("--pw", help="Control password", required=True)
args = parser.parse_args()

port = args.port
host = args.host
pw = args.pw

main()
    
