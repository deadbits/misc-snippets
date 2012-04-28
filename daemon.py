#!/usr/bin/python
# creates daemon
# must use the double fork so the terminal isn't taken over
# atleast i think so..if i'm wrong, someone let me know


import os
import sys


def daemon(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
    try: 
        pid = os.fork() 
        if pid > 0:
            sys.exit(0) 
    except OSError, e: 
        print >>sys.stderr, "[!] fork one failed: %d (%s)" % (e.errno, e.strerror) 
        sys.exit(1)

    os.chdir("/") 
    os.setsid() 
    os.umask(0) 

    try: 
        pid = os.fork() 
        if pid > 0:
            print "[*] Daemon PID: %d" % pid 
            sys.exit(0) 
    except OSError, e: 
        print >>sys.stderr, "[!] fork two failed: %d (%s)" % (e.errno, e.strerror) 
        sys.exit(1) 

    si = file(stdin, 'r')
    so = file(stdout, 'a+')
    se = file(stderr, 'a+', 0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())
