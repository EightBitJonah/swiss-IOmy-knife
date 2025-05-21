import time,logging,os,sys
import nmap
from datetime import datetime
from tenable.io import TenableIO

__location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Set up logging
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_file = os.path.join(log_dir, 'nmapper_scans.txt')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(log_file)  # Only log to file
    ]
)

logger = logging.getLogger('nmapper')

# Import Database class using importlib to avoid path issues
import importlib.util
spec = importlib.util.spec_from_file_location("database", os.path.join(os.path.dirname(os.path.dirname(__file__)), "db", "database.py"))
database = importlib.util.module_from_spec(spec)
spec.loader.exec_module(database)
Database = database.Database

def nmapper():
    # Get API keys
    db = Database('swissknife.db')
    access_key, secret_key = db.get_api_key('tenable')
    db.close()
    
    tio = TenableIO(access_key, secret_key)
    
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
            logger.info(f"No live hosts found in scan of {targets}")
            print("No live hosts found")
            return
            
        # Log detailed host list to file but keep console output minimal
        logger.info(f"Found live hosts: {', '.join(targets)}")
        print(f"Found {len(targets)} live hosts")
        print("Adding hosts to scan...")
          # Store targets in database
        db = Database('swissknife.db')
        db.store_nmap_targets(scan, targets)
        print('Adding targets to scan...')
        # Get targets from database and update scan
        targets_list = db.get_nmap_targets(scan)
        try:
            # Keep detailed logging in file only
            logger.info(f"Sending targets to Tenable.io scan {scan}")
            logger.info(f"Payload: {targets_list}")
            
            # Make the API call
            print("Updating scan targets...")
            response = tio.scans.configure(scan, targets=targets_list)
            
            # Log full response to file
            logger.info(f"Tenable.io API Response: {str(response)}")
            print("Successfully updated scan targets.")
            
        except Exception as e:
            logger.error(f"Tenable.io API Error: {str(e)}")
            print("\nAn error occurred while updating the scan.")
            print("For details, check the log file at: logs/nmapper_scans.txt")
        
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
        logger.error("Error running nmap scan. Make sure nmap is installed correctly.")
        print("Error running nmap scan. Make sure nmap is installed correctly.")
        return
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        print("An error occurred during the scan.")
        print("For details, check the log file at: logs/nmapper_scans.txt")
        return