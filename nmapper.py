# import modules
from tenable.io import TenableIO
import subprocess,sys,time,logging,os
windowsuser = os.name == 'nt'
nixuser = os.name == 'posix' 

if windowsuser : 
    print("This script does not support Windows.")
    exit()

# define variables
accesskey = input("Enter your Access Key: ")
secretkey = input("Enter your Secret Key: ")
tio = TenableIO(accesskey,secretkey)
scan = input("Please provide the scan ID that you would like to update: ")
targetdir = input("Enter destination for Targets file: " )
targets = input("Please provide a CIDR range to scan: ")
   

print('Using these settings...' + '\n' + 'Scan ID ' + scan + '\n' + 'Targets ' + targets)
 
# Defining nmap scan + target output
NMAPPER = "nmap -n -sn " + targets + " -oG - | awk '/Up$/{print $2}' > " + targetdir + "/targets.txt"
# NMAPPERWIN = "nmap -n -sn " + targets + " -oG - | ForEach-Object { if ($_ -match 'Host: (\S+)') { $Matches[1] } } | Out-File " + targetdir + "/targets.txt"

time.sleep(5)   

print('Starting nmap scan!')

if nixuser :
    subprocess.call(NMAPPER, shell=True)
    if "Nmap done" :
        print('nmap scan complete, reading target list...')
    else :
        print("nmap is not installed")
        exit()
#elif windowsuser : 
    #subprocess.run(NMAPPERWIN, shell=True)
    #if "Nmap done" :
    #    print('nmap scan complete, reading target list...')
    #else :
    #    print("nmap is not installed")
# removing Windows support
#    print("This script does not support Windows.")
#        exit()

#defining target list to read
mytargets = open(targetdir + "/targets.txt","r")
content = mytargets.read()
content_list = content.split(",")
mytargets.close()

print('Adding targets to scan...')

#update scan
tio.scans.configure(scan,
targets=content_list
)


print('Success!')
