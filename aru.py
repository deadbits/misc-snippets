#!/usr/bin/env python
#
# automated recon utility - version 1.0
# automation for SubBrute script by TheRook and nmap
# place this in the same directory as subbrute.py
# supply a domain name and an output file.
# subdomain bruteforce is performed and all hosts are scanned
# ~ ohdae

import os
import sys
import commands


def banner():
	print("\n\t       automated recon utility [v1.0]")
	print("\t  usage: ./aru.py <domain> <output file>")
	print("\texample: ./aru.py hackmeplz.com woot.txt\n")


def run_subbrute(host):
	found_domains = []
	if os.path.exists("subbrute.py") is False:
		print("[error] subbrute was not found in this directory.")
		sys.exit(1)

	print("[~] starting sub-domain bruteforce on %s. be patient..." % host)
	sub_output = commands.getoutput("python subbrute.py -r resolvers.txt -s subs.txt %s" % host).split("\n")
	if subs_output is not "":
		try:
			for domains in subs_output:
				found_domains.append(domains)
				print("[~] added %s to scan queue." % domains)
		except:
			pass
	else:
		print("[error] no sub-domains found for %s" % domain)
	print("[~] starting nmap scans on discoverd domains...")
	run_nmap(found_domains, output_file)


def run_nmap(found_domains, output_file):
	fout = open(output_file, "rb")

	for host in found_domains:
		print("[~] scanning %s" % host)
		nmap_out = commands.getoutput("nmap -PN %s" % host).split("\n")
		for lines in nmap_out:
			output.write(lines)

	print("[*] scans complete.")
	print("[*] output file: %s" % output_file)


try:
	domain = sys.argv[1]
	fout = sys.argv[2]
	run_subbrute(domain)
except IndexError:
	banner()







