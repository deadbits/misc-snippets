#!/usr/bin/env python
##
# pastebin cli utility
# author: ohdae (ams) - 2013
# https://github.com/ohdae/misc-snippets
##

import sys
import os
import requests
import urllib
import argparse

class Pastebin(object):
    def __init__(self):
        self.host = 'http://pastebin.com/api/api_post.php'
        self.headers = { 'User-Agent': 'https://github.com/ohdae/pastebin', 'Content-Type': 'application/x-www-form-urlencoded', 'Accept': 'text/plain' }
        self.api_key = 'replace with your developer API key'

    def trends(self):
        """
        import pastebin
        print('retrieving trending post list ...')
        trends = Pastebin.trends
        for entry in trends:
            print entry
        """
        print("[+] retrieving trending post list ...")
        data = { 'api_option': 'trends', 'api_user_key': '', 'api_dev_key': self.api_key }
        data = urllib.urlencode(data)
        req = requests.post(self.host, params=data, headers=self.headers)
        result = []
        if req.status_code == 200:
            print('Results: ')
            content = req.content.split('\n')
            for lines in content:
                result.append(lines)
        else:
            print('[error] failed to retrieve trending posts!')
            sys.exit(1)

    def paste(self, content, format, name):
        """
        import pastebin
        pastebin_url = Pastebin.paste("filename.txt", "python", "my sample post!")
        print("Post URL: %s" % pastebin_url)
        """
        print('[+] reading input file ...')
        data = ''
        if not os.path.exists(content):
            print('[error] input file %s not found!' % content)
            sys.exit(1)
        fin = open(content, 'rb')
        for line in fin.readlines():
            data += line
        print('[+] building http request ...')
        p = {
            'api_option': 'paste',
            'api_user_key': '',
            'api_paste_private': 1,
            'api_paste_name': content,
            'api_paste_expire_date': 'N',
            'api_paste_format': format,
            'api_dev_key': self.api_key,
            'api_paste_code': data
        }
        p = urllib.urlencode(p)
        print('[+] sending post to pastebin ...')
        req = requests.post(self.host, params=p, headers=self.headers)
        if req.status_code == 200:
            print('[*] pastebin post accepted!')
            return req.content
        else:
            print('[error] pastebin post failed. please try again.')
            sys.exit(1)


help = """pastebin utility - https://github.com/ohdae/misc-snippets"""
parser = argparse.ArgumentParser(description=help, prog='pastebin.py')
parser.add_argument('--content', help='post content')
parser.add_argument('--name', help='post title')
parser.add_argument('--format', help='syntax format')
parser.add_argument('--trends', help='display trending posts', action='store_true')
args = parser.parse_args()

Pastebin = Pastebin()

if args.content:
    content = args.content
    if not args.name:
        post_name = content
    else:
        post_name = args.name
    if args.format:
        format = args.format
    else:
        format = 'text'
    post_id = Pastebin.paste(content, format, post_name)
    print('[*] Pastebin URL: %s' % post_id)
if args.trends:
    trending = Pastebin.trends()
    if trending is not None:
        for entry in trending:
            print entry

