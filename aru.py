#!/usr/bin/env python
# automated recon utility [v1.2]
# ohdae - 2013
# https://github.com/ohdae/misc-snippets
#
# designed for use with SubBrute by TheRook
# this script automates the subbrute process
# and then perform a quick nmap scan of each subdomain
# that is found. make note that some of the subdomains
# might be vhosts and therefore have the same nmap output.
# this isn't anything innovative. it's just something i use myself.

import os
import argparse
import commands
import sys

def nmap(h):
    print('starting nmap scan of %s ...' % h)
    try:
        nout = open(scans, 'wb')
        raw = commands.getoutput('nmap -sS -sV -PN -T5 %s' % h).split('\n')
        for l in raw:
            if only_open:
                if 'open' in l:
                    nout.write(l)
            else:
                nout.write(l)
        nout.write('\n\n')
        nout.close()
    except:
        print('[error] failed to nmap %s' % h)

def brute():
    s = sub_path+'subbrute.py'
    r = sub_path+'resolvers.txt'
    l = sub_path+'subs.txt' 
    hout = open(hosts, 'wb')
    print('starting sub-domain recon for %s. be patient ...' % host)
    subs = commands.getoutput('python %s -r %s -s %s %s' % (s, r, l, host)).split('\n')
    for h in subs:
        if h is not "":
            hout.write(h)
            nmap(h)
    print('\nautomated recon completed!')
    print('sub-domains found: %s' % hosts)
    print(' nmap scan results: %s' % scans)


help = """automated recon utility - place in the same directory as subbrute.py"""
parser = argparse.ArgumentParser(description=help, prog='aru.py')
parser.add_argument('--target', help='target', required=True)
parser.add_argument('--open', help='only log open ports [default on]', default=True)
parser.add_argument('--path', help='subbrute [ex: /pentest/subbrute', required=True)
args = parser.parse_args()
host = args.target
only_open = args.open
sub_path = args.path

if not sub_path[-1:] == '/':
    sub_path = sub_path + '/'
if not os.path.exists(sub_path+'subbrute.py'):
    print('[error] subbrute.py not found in %s' % sub_path)
    sys.exit(1)
if os.path.exists('./%s' % host):
    print('[error] ./%s exists. did you all ready scan this domain?' % host)
    sys.exit(1)
os.mkdir('./%s' % host)
hosts = './%s/hosts.txt' % host
scans = './%s/nmap.txt' % host
os.system('touch %s' % hosts)
os.system('touch %s' % scans)
brute()

