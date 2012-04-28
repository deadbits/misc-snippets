#!/usr/bin/python
#
# see @vorbis for original implementation
#
# [author: ohdae]
# socat tunnel helper script

import os
import argparse

def whereis():
    program = 'socat'
    for path in os.environ.get('PATH', '').split(':'):
        if os.path.exists(os.path.join(path, program)) and \
            not os.path.isdir(os.path.join(path, program)):
                return os.path.join(path, program) 
    return None

if whereis() is None:
    print("[!] socat is not installed!")
    sys.exit()


help = """socat helper. setups a tunnel through localhost to a remote destination with socks4a proxy support"""

parser = argparse.ArgumentParser(description=help, prog="sctunnel")
parser.add_argument("--lport", help="Local port", type=int, required=True)
parser.add_argument("--dst", help="Destination IP/host", required=True)
parser.add_argument("--dport", help="Destination port", type=int, required=True)
parser.add_argument("--socks", help="SOCKS port, defaults to TOR", default=9050, type=int)
args = parser.parse_args()

lport = args.lport
dst = args.dst
dport = args.dport
sport = args.socks

os.system("socat TCP4-LISTEN:%d,fork SOCKS4A:localhost:%s:%d,socksport=%d &" % (lport, dst, dport, sport))
print("[*] Listener started!")
print("   Destination: %s:%d" % (dst, dport))
print("   Listener: localhost:%d" % lport)
print("   SOCKS port: %d" % sport)



