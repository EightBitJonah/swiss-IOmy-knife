import subprocess,time,logging,os,sys



__location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))) 

# API Keys are defined in a txt file
accessfile = open(os.path.join(__location__, '..','accesskey.txt'))
accesskey = accessfile.read()
accessfile.close()

secretfile = open(os.path.join(__location__, '..','accesskey.txt'))
secretkey = secretfile.read()
secretfile.close()

#targetfile = open(os.path.join(__location__, 'targets.txt'))

from tenable.io import TenableIO
tio = TenableIO('{accesskey}','{secretkey}')


windowsuser = os.name == 'nt'
nixuser = os.name == 'posix' 

def nmapper() :
        if windowsuser : 
            print("This script does not support Windows, returning to SwissCore")
            time.sleep(3)
            return
    
        
        scan = input("Please provide the scan ID that you would like to update: ")
        targetdir = input("Enter destination for Targets file: " )
        targets = input("Please provide a CIDR range to scan: ")
        

        print('Using these settings...' + '\n' + 'Scan ID ' + scan + '\n' + 'Targets ' + targets)
        
 

            

        # Defining nmap scan + target output
        NMAPPER = "nmap -n -sn " + targets + " -oG - | awk '/Up$/{print $2}' > " + targetdir + "/targets.txt"
        #NMAPPERWIN = "nmap -n -sn " + targets + " -oG - | powershell ForEach-Object { if ($_ -match 'Host: (\S+)') { $Matches[1] } } > " + targetdir

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


        #defining target list to read
        mytargets = open(targetdir,"r")
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