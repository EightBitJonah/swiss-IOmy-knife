import subprocess,time,logging,os,sys

__location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))) 

nmapperfolder = os.path.dirname(os.path.abspath(__file__))
targetfile = os.path.join (nmapperfolder, 'targets.txt')


# Import Database class using importlib to avoid path issues
import importlib.util
spec = importlib.util.spec_from_file_location("database", os.path.join(os.path.dirname(os.path.dirname(__file__)), "db", "database.py"))
database = importlib.util.module_from_spec(spec)
spec.loader.exec_module(database)
Database = database.Database

# Get API keys from database
db = Database('swissknife.db')
keys = db.get_api_key('tenable')
if not keys:
    print("No Tenable.io API keys found. Please set them up in the API Key Management menu.")
    sys.exit(1)
access_key, secret_key = keys
db.close()

from tenable.io import TenableIO
tio = TenableIO(access_key, secret_key)


windowsuser = os.name == 'nt'
nixuser = os.name == 'posix' 

def nmapper() :
        if windowsuser : 
            print("This script does not support Windows, returning to SwissCore")
            time.sleep(3)
            return
        
        scan = input("Please provide the scan ID that you would like to update: ")
        targets = input("Please provide a CIDR range to scan: ")
        

        print('Using these settings...' + '\n' + 'Scan ID ' + scan + '\n' + targetfile + '\n'  'Targets ' + targets)
        print('Are these settings correct? Y/N')
        nmappernext = input('> ')
        if nmappernext == ["Y"] :
            print('Starting nmap scan!')
            #settings_menu = False
        elif nmappernext == ["N"] :
            print("Returning to settings input...")
            nmapper()           

        # Defining nmap scan + target output
        NMAPPER = "nmap -n -sn " + targets + " -oG - | awk '/Up$/{print $2}' > " + targetfile 
        NMAPPERWIN = f"nmap -n -sn {targets} -oG - | powershell ForEach-Object {{ if ($_ -match 'Host: (\S+)') {{ $Matches[1] }} }} > {targetfile}" 

        time.sleep(5)   

        

        if nixuser :
            subprocess.call(NMAPPER, shell=True)
            if "Nmap done" :
                print('nmap scan complete, reading target list...')
            else :
                print("nmap is not installed")
                exit()
        elif windowsuser : 
            result = subprocess.Popen([NMAPPERWIN], stdout=subprocess.PIPE, shell=True)
            result.stdout
            if "Nmap done" :
                print('nmap scan complete, reading target list...')
            else :
                print("nmap is not installed")
                exit()

        print(f"Reading targets from {targetfile}...")
        #defining target list to read
        mytargets = open(targetfile, 'r')
        content = mytargets.read()
        content_list = content.split(',')
        mytargets.close()

        print('Adding targets to scan...')

        #update scan
        tio.scans.configure(scan,
        targets=content_list)
        


        print('Success!')
        print('Would you like to run another nmap scan? Y/N')
        nmappernext
        if nmappernext == ["Y"] :
            nmapper()
        elif nmappernext == ["N"] :
            return






#if __name__ == "__nmapper__" : 
#        nmapper()