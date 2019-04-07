#!/usr/bin/env python3
###
# Collect AlienVault Reputation DB entries and send over syslog
# Updated for Py3.7 for better error handling, etc, etc. but it doesnt run
# because of an error I really dont care enough to debug.
###

import time
import socket
import requests


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
                    addr, info = d[0].rstrip(), d[1].lstrip()
                    print(f'[~] sending syslog event for {info} - {addr}')
                    cef = f'CEF:0|OSINT|AlienVault Reputation DB|1.0|100|{info}|1|src_ip={addr} msg={info} source={config["otx"]}'
                    res = send_syslog(cef)
                    if res:
                        count += 1
                except IndexError:
                    continue

    except Exception as err:
        print(f'[!] error retrieving otx database: {err}')
        return count

    return count


if __name__ == '__main__':
    print('\n\n\t open-source data gathering ')
    print('\t   source >> AlienVault OTX   \n\n')


while True:
    try:
        print("[~] starting collecting of AlienVault reputation database...")
        count = gather_data()
        print(f'[*] {count} unique events sent over syslog')
        print('[-] sleeping for 60 minutes until next collection...')
        time.sleep(3600)

    except KeyboardInterrupt:
        print('[!] caught KeyboardException by user. ending loop.')
        break

    except Exception as err:
        print(f'[!] caught unhandled exception: {err}')
        raise err
