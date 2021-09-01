from tenable.io import TenableIO
tio = TenableIO('8c12312f249b7d91f489553937d81d5f6df9fb092e64dec1fb81b8516e8928c1','593283af59d2067a93e98e7c44d8bf915578140b083d1a6dd193b03001da2b24')

import subprocess, datetime

#Defining nmap scan + target output
NMAPPER = "nmap -n -sn 10.0.0.0/24 -oG - | awk '/Up$/{print $2}' > /Users/jmpeterson/documents/targets.txt"

print('Starting nmap scan!')
subprocess.call(NMAPPER, shell=True)
if "Nmap done" :
    print('nmap scan complete, reading target list...')
else :
    print("nmap is not installed")
    exit()


#defining target list to read
mytargets = open("/Users/jmpeterson/documents/targets.txt","r")
content = mytargets.read()

content_list = content.split(",")
mytargets.close()

print('Adding targets to scan...')

#update scan
tio.scans.configure(108,
targets=content_list
)


print('Success!')
