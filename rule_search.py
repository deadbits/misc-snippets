#!/usr/bin/python

import os, sys
import requests

## Define globals
search_one = "http://www.snort.org/search/sid"

## Splits user-input into proper format
def split_input(rule):
    if ":" in rule:
        try:
            rule = rule.split(":")
            sid = rule[1]

            if rule[0] == "1":
                param = ("%s?r=1" % sid)
                rule_search(param, sid)
            else:
                sid_one = rule[0]
                param = ("%s?r=%s" % (sid, sid_one))
                rule_search(param, sid)
        except:
            print("[!] invalid rule input!")
            sys.exit(0)

    elif "-" in rule:
        try:
            rule = rule.split("-")
            sid = rule[1]

            if rule[0] == "1":
                param = ("%s?r=1" % sid)
                rule_search(param, sid)
            else:
                sid_one = rule[0]
                param = ("%s?r=%s" % (sid, sid_one))
                rule_search(param, sid)
        except:
            print("[!] invalid rule input!")

    else:
        param = ("%s?r=1" % rule)
        rule_search(param, rule)


## Remove any temporary files we created
def clean_up():
    if os.path.exists("%s.html" % sid):
        os.system("rm %s.html" % sid)
    else:
        pass

## Performs the actual search for our Snort SID
def rule_search(req_value, sid):
    print("[*] Searching Snort database for SID %s...\n" % sid)
    output = requests.get("%s/%s" % (search_one, req_value))
    
    tmp = file("%s.html" % sid, "w")
    tmp.write(output.content)
    tmp.close()
    tmp = file("%s.html" % sid, "r")

    print("Rule ID: %s" % sid)
    for l in tmp.readlines():

        if '<p class="detailed_information">' in l:
            summary = l.split(">")
            summary = summary[1].split("<")[0]
            print("Description: %s\n" % summary)

        elif '<li class="affected_systems">' in l:
            affects = l.split(">")
            affects = affects[1].split("<")[0]
            print("Affected Systems: %s\n" % affects)


rule_req = raw_input("SourceFire Rule SID: ")

if rule_req.isdigit():
    split_input(rule_req)
else:
    print("[!] Rule SID must be a digit!")
    sys.exit(0)

