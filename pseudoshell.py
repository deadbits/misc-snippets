#!/usr/bin/env python

import subprocess
import sys


def cmdexec(cmd):
    p = subprocess.Popen(cmd, shell = True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)  
    stdout = []

    while True:
        out = p.stdout.readline()
        stdout.append(out)
        print out
        if out == "" and p.poll() != None:
            break
            
    return ''.join(stdout)


def about():
    print("\nThis is an example of using Python's subprocess module and readline to view command output in real-time.")
    print("Instead of waiting for the command to execute, capturing the output and displaying it, you can get streaming results.")
    print("Using this method will let you run interactive and streaming commands such as ping, tracert, sudo and more.")
    print("Use the prompt below to enter commands. To exit the prompt, enter :exit")
    print("woot.\n")
    

about()
while True:
    cmd = raw_input("command >> ")
    if cmd == ":exit":
        sys.exit(0)
    else:
        cmdexec(cmd)

