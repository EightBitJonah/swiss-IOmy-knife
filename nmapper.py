# import modules
from tenable.io import TenableIO
import subprocess,sys,time,logging,os

# define variables
accesskey = input("Enter your Access Key: ")
secretkey = input("Enter your Secret Key: ")
tio = TenableIO(accesskey,secretkey)
scan = input("Please provide the scan ID that you would like to update: ")
targetdir = input("Enter destination for Targets file: " )
targets = input("Please provide a CIDR range to scan: ")
windowsuser = os.name == 'nt'
nixuser = os.name == 'posix'    

print('Using these settings...' + '\n' + 'Scan ID ' + scan + '\n' + 'Targets ' + targets)
 
# Defining nmap scan + target output
NMAPPER = "nmap -n -sn " + targets + " -oG - | awk '/Up$/{print $2}' >" + targetdir + "/targets.txt"
NMAPPERWIN = "nmap -n -sn " + targets + " -oG - | ForEach-Object { if ($_ -match 'Host: (\S+)') { $Matches[1] } } | Out-File" + targetdir + "/targets.txt"

time.sleep(5)   

print('Starting nmap scan!')

if nixuser :
    subprocess.call(NMAPPER, shell=True)
    if "Nmap done" :
        print('nmap scan complete, reading target list...')
    else :
        print("nmap is not installed")
        exit()
elif windowsuser : 
    subprocess.run(NMAPPERWIN])
    if "Nmap done" :
        print('nmap scan complete, reading target list...')
    else :
        print("nmap is not installed")
        exit()

#defining target list to read
mytargets = open("targets.txt","r")
content = mytargets.read()
content_list = content.split(",")
mytargets.close()

print('Adding targets to scan...')

#update scan
tio.scans.configure(scan,
targets=content_list
)


print('Success!')
