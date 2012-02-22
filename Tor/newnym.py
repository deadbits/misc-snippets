#!/usr/bin/python

# Get new TOR Identity

import telnetlib
import time

def newnym():
    tn = telnetlib.Telnet('localhost', 9051)
    tn.write(('AUTHENTICATE "test"\r\n'))
    res = tn.read_until('250 OK', 5)
    if res.find('250 OK') > -1:
       print('AUTHENICATE accepted.')
    tn.write("signal NEWNYM\r\n")
    res = tn.read_until('250 OK', 5)
    if res.find('250 OK') > -1:
       print("[+] New identity successfull")
    
    
while(True):
   time.sleep(90)
   newnym()   
   print("[+] New identity in 90 seconds...")
     
newnym()       
   
    
