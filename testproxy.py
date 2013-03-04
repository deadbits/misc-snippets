#!/usr/bin/env python
##
# quickly test your proxies.
# https://github.com/ohdae/misc-snippets
# socks test usage: ./testproxy.py --host 127.0.0.1 --port 9050 --type socks
#  http test usage: ./testproxy.py --host 127.0.0.1 --port 8118 --type http
##

import requests
import argparse

class ProxyTest:
    def __init__(self):
        self.user_agent = { 'User-Agent': 'Proxy Test (https://github.com/ohdae/misc-snippets)' }

    def get_ip(self, proxy):
        result = requests.get('http://www.ifconfig.me/ip', proxies=proxy, headers=user_agent).content
        return result

    def socks(self, host, port):
        proxy = { 'http': 'socks5://%s:%s' % (host, port), 'https': 'socks5://%s:%s' % (host, port) }
        print('[*] Testing SOCKS5 proxy => %s:%s' % (host, port))
        print('SOCKS IP: %s' % self.get_ip(proxy))

    def http(self, host, port):
        proxy = { 'http': '%s:%s' % (host, port), 'https': '%s:%s' % (host, port) }
        print('[*] Testing HTTP proxy => %s:%s' % (host, port))
        print('HTTP IP: %s' % self.get_ip(proxy))

help = """proxy test helper - https://github.com/ohdae/misc-snippets"""
parser = argparse.ArgumentParser(description=help, prog='testproxy.py')
parser.add_argument('--host', help='proxy host', required=True)
parser.add_argument('--port', help='proxy port', required=True)
parser.add_argument('--type', help='proxy type', choices=['socks', 'http'], required=True)
args = parser.parse_args()
Proxy = ProxyTest()

print('Public IP:\t%s' % requests.get('http://www.ifconfig.me/ip').content)
if args.type.lower() == 'socks':
    Proxy.socks(args.host, args.port)
if args.type.lower() == 'http':
    Proxy.http(args.host, args.port)
