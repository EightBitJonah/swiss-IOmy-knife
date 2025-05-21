import time,logging,os,sys
import nmap

__location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

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

def nmapper():
        scan = input("Please provide the scan ID that you would like to update: ")
        targets = input("Please provide a CIDR range to scan: ")
        
        print('Using these settings...' + '\n' + 'Scan ID ' + scan + '\n' + 'Targets ' + targets)
        print('Are these settings correct? Y/N')
        nmappernext = input('> ').upper()
        if nmappernext == "Y":
            print('Starting nmap scan!')
        elif nmappernext == "N":
            print("Returning to settings input...")
            nmapper()
            return

        print("Running nmap scan...")
        nm = nmap.PortScanner()
        try:
            # Run a ping scan (-sn) with no DNS resolution (-n)
            nm.scan(hosts=targets, arguments='-n -sn')
            
            # Get list of all hosts that are up
            targets = [host for host in nm.all_hosts() if nm[host].state() == 'up']
            
            if not targets:
                print("No live hosts found")
                return

            print(f"Found {len(targets)} live hosts")
            print("Storing targets in database...")
            
            # Store targets in database
            db = Database('swissknife.db')
            db.store_nmap_targets(scan, targets)
            
            print('Adding targets to scan...')
            # Get targets from database and update scan
            targets_list = db.get_nmap_targets(scan)
            tio.scans.configure(scan, targets=targets_list)
            
            # Clean up the targets from database since they're now in the scan
            db.delete_nmap_targets(scan)
            db.close()

            print('Success!')
            print('Would you like to run another nmap scan? Y/N')
            nmappernext = input('> ').upper()
            if nmappernext == "Y":
                nmapper()
            elif nmappernext == "N":
                return
                
        except nmap.PortScannerError:
            print("Error running nmap scan. Make sure nmap is installed correctly.")
            return
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return