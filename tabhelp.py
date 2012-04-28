#!/usr/bin/python
# 
# simple TabNanny automation
# feed it a file and it calls tabnanny and shows results
# displays tabs, spaces, newlines, etc.

import tabnanny
import sys

if len(sys.argv) <=1:
	print("Tabnanny Helper Script")
	print("What => This script checks for the existence of tabs and indents within a specified Python script.")
	print("Why => Python is a crappy whitespace language and will throw errors if you mix spaces and tabs.")
	print("How => Enter the filename that you would like to check. Review it. Proceed to curse Python and then go write some Ruby.")	
	print("usage: ./tabhelper.py filename")
	sys.exit()	

filename = sys.argv[1]

file = open(filename)
for line in file.readlines():
	print repr(line)
