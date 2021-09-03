import subprocess,time,logging,os,sys
from tenable.io import TenableIO

__location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))) 

# API Keys are defined in a txt file
apikeysfile = open(os.path.join(__location__, '..','apikeys.txt'))
apikeys = apikeysfile.read()
apikeysfile.close()

windowsuser = os.name == 'nt'
nixuser = os.name == 'posix' 

def nmapper() :
        if windowsuser : 
            print("This script does not support Windows, returning to SwissCore")
            time.sleep(3)
            return
    
        # define variables

        tio = TenableIO(apikeys)

        scan = input("Please provide the scan ID that you would like to update: ")
        targetdir = input("Enter destination for Targets file: " )
        targets = input("Please provide a CIDR range to scan: ")
        

        print('Using these settings...' + '\n' + 'Scan ID ' + scan + '\n' + 'Targets ' + targets)
        
        # Defining nmap scan + target output
        NMAPPER = "nmap -n -sn " + targets + " -oG - | awk '/Up$/{print $2}' > " + targetdir + "/targets.txt"
        # NMAPPERWIN = "nmap -n -sn " + targets + " -oG - | powershell ForEach-Object { if ($_ -match 'Host: (\S+)') { $Matches[1] } } > " + targetdir + "\targets.txt"

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
        #    subprocess.run(NMAPPERWIN, shell=True)
        #    if "Nmap done" :
        #        print('nmap scan complete, reading target list...')
        #    else :
        #        print("nmap is not installed")
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


if __name__ == "__nmapper__" : 
        nmapper()