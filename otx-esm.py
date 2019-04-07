#!/usr/bin/env python3
## @NOTE: NOT DONE - DO NOT USE
###
# Collect AlienVault OTX reputation DB entries and send over syslog
# Updated for Py3.7
# --
# originally the stand-alone version from ArcReactor (an awful old project, dont look at it. really.)
###

import re
import sys
import time
import socket
import requests

from tqdm import tqdm


config = {
    'otx': 'http://reputation.alienvault.com/reputation.snort',
    'host': '127.0.0.1',
    'port': '512'
}


def send_syslog(msg):
    """ Send a syslog message to defined host and port 
    
    @param msg: message
    @type str
    
    @note: %d in the syslog msg is the syslog level + facility * 8
         data = '<%d>%s' % (level + facility*8, message)
         change this if you feel the need
    """
    res = False

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        data = f'<29>{msg}'
        sock.sendto(data, (config['host'], int(config['port'])))
        sock.close()
        res = True
    except Exception as err:
        print(f'[!] failed to send syslog message: {err}')

    return res


def gather_data():
    count = 0 

    data = requests.get(config['otx']).content
    
    try:
        print('[~] attempting to parse reputation data ...')
        for line in data.split('\n'):
            if not line.startswith('#') and line != '':
                try:
                    # snort format is: ip-address # message
                    d = line.split("#")
                    addr, info = d[0], d[1]
                    print(f'[~] sending syslog event for {info} - {addr}')
                    cef = f'CEF:0|OSINT|OTX|1.0|100|{info}|1|src={addr} msg={config["otx"]}'
                    res = send_syslog(cef)
                    if res:
                        count += 1
                except IndexError:
                    continue

    except Exception as err:
        print(f'[!] error retrieving otx database: {err}')
        return count

    return count

print("\n\n")
print("\t open-source data gathering ")
print("\t   source >> AlienVault OTX   ")
print("\n\n")

print("[~] starting collecting of OTX reputation database...")


while True:
    try:
        count = gather_data()
        print(f'[*] {count} unique events sent from OTX')
        print('[-] sleeping for 60 minutes ...')
        for i in tqdm(range(10)):
            time.sleep(3600)
    except KeyboardException:
        print('[!] caught KeyboardException by user. ending loop.')
        break
