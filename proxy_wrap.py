#!/usr/bin/env python
##
# class wrapper for proxy configurations 
# original code by fitblip (http://www.talesofacoldadmin.com/)
# all i did was a little rewriting and wrapping it in a class
# for easier usage.
#
# https://github.com/ohdae/misc-snippets
##

from socket import *
import socks
import requests

class Proxy(object):
  def __init__(self):
		self.orig_sock = socket
		self.running = False

	def getaddrinfo(self, *args):
		"""
		simple monkey patch for DNS proxying
		"""
		return [(AF_INET, SOCK_STREAM, 6, '', (args[0], args[1]))]
	getaddrinfo = self.getaddrinfo

	def set(self, type=socks.PROXY_TYPE_SOCKS5, host='127.0.0.1', port='9050'):
		"""
		configure and active current proxy. change arguments as needed
		"""
		socks.setdefaultproxy(type, host, port)
		self.socket = socks.socksocket
		self.running = True

	def unset(self):
		"""
		returns socket to original state (no proxy)
		"""
		self.socket = self.orig_sock
		self.running = False

	def is_tor(self):
		"""
		checks if tor is properly enabled
		"""
		if "Sorry" in requests.get('https://check.torproject.org/').content():
			return False
		return True

	def tor_newnym(self, control_host='127.0.0.1', control_port=9051, password):
		self.s = socket()
		self.s.connect((control_host, control_port))
		self.s.send('Authenticate %s\r\n' % password)
		if not '250' in self.s.recv(1024):
			return False
		self.s.send('signal newnym\r\n')
		if not '250' in self.s.recv(1024):
			return False
		self.s.close()
		return True			

	def get_ip(self):
		"""
		gather and return current ip address
		"""
		self.current_ip = requests.get('http://ifconfig.me/ip').content().strip()
		return self.current_ip

if __name__ == '__main__':
	proxy = Proxy()

	"""
	setup TOR SOCKS5 proxy =>
	print('[*] setting socks5 proxy 127.0.0.1:9050')
	proxy.set(type=socks.PROXY_TYPE_SOCKS5, host='127.0.0.1', port=9050)
	if proxy.is_tor:
		print('[+] tor proxy running!')
		print('[*] triggering newnym in 30 seconds ...')
		import time; time.sleep(30)
		if not proxy.tor_newnym('mypassword'):
			print('[!] failed to get newnym!')
		print('[+] newnym sent successfully!')
	else:
		print('[!] tor proxy is not running correctly!')
	print('IP Address: %s' % proxy.get_ip)

	setup SOCKS5 proxy on port 4444 =>
	print('[*] setting socks5 proxy 127.0.0.1:4444')
	proxy.set(type=socks.PROXY_TYPE_SOCKS5, host='127.0.0.1', port=4444)
	print('IP Address: %s' % proxy.get_ip)

	disable currently running proxy =>
	print('[*] disabling proxy')
	if proxy.running:
		proxy.unset()
	else:
		print('[!] proxy does not appear to be running!')
	print('IP Address: %s' % proxy.get_ip)
	"""

