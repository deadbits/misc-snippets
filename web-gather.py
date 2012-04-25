#!/usr/bin/python
# Gathers links and email addresses from a given url
# author: ohdae
# bindshell.it.cx

import urllib2
import argparse
import os, re

def getemails():
    emails = []
    pattern = re.compile("[-a-zA-Z0-9._]+@[-a-zA-Z0-9_]+.[a-zA-Z0-9_.]+")
    emails = re.findall(pattern, html_read)
    for items in emails:
        storelinks.write("[ Email ] %s\n" % items)


def getlinks():
    links = []
    for url in html_read.split():
        if 'http://' in url:
            if 'href=' in url:
                urls = url.lstrip('href=').split('>')
                for i in urls:
                    if 'http://' in i:
			storelinks.write(i.lstrip("'\"").rstrip("'\"")+"\n")
        else:
            continue

help = """Pull linked url's and emails from a given website and saved them into a text document"""

parser = argparse.ArgumentParser(description=help)
parser.add_argument("--www", help="target website", required=True)
parser.add_argument("--save", help="save file", required=True)
parser.add_argument("--email", help="finds emails", choices=["yes", "no"], required=False)

args = parser.parse_args()
target = args.www
saved = args.save

url_html = urllib2.urlopen(target)
html_read = url_html.read()
storelinks = open(saved, "a")
getlinks()

if args.email == "yes":
    getemails()
    print("[+] Complete!")
else:
    print("[+] Complete!")

