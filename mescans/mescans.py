import os,sys,time,pprint,re
from tabulate import tabulate
from tenable.io import TenableIO

# Import Database class using importlib to avoid path issues
import importlib.util
spec = importlib.util.spec_from_file_location("database", os.path.join(os.path.dirname(os.path.dirname(__file__)), "db", "database.py"))
database = importlib.util.module_from_spec(spec)
spec.loader.exec_module(database)
Database = database.Database

def mescans():
    # Get API keys
    db = Database('swissknife.db')
    access_key, secret_key = db.get_api_key('tenable')
    db.close()
    
    tio = TenableIO(access_key, secret_key)
    
    try:
        # Get scan list from API
        raw_scans = tio.scans.list()
        
        # Process scan data into clean format
        scans = []
        for scan in raw_scans:
            try:
                # Extract scan details - handle both dict and object access
                name = scan.get('name', None) if hasattr(scan, 'get') else getattr(scan, 'name', None)
                scan_id = scan.get('id', None) if hasattr(scan, 'get') else getattr(scan, 'id', None)
                owner = scan.get('owner', '') if hasattr(scan, 'get') else getattr(scan, 'owner', '')
                
                # Skip scans with missing required data
                if not all([name, scan_id, owner]):
                    continue
                    
                # Extract username from email
                owner = owner.split('@')[0] if '@' in owner else owner
                
                scans.append({
                    'name': name,
                    'owner': owner,
                    'id': scan_id
                })
            except Exception as e:
                print(f"Warning: Could not process scan: {e}")
                continue
            
        if not scans:
            print("\nNo scans found or could not process scan data.")
            return
            
        # Sort scans by name
        scans.sort(key=lambda x: str(x['name']).lower())
        
        # Calculate column widths
        max_name = max(len(str(scan['name'])) for scan in scans)
        max_owner = max(len(str(scan['owner'])) for scan in scans)
        name_width = min(60, max(20, max_name + 2))  # Cap name width at 60 chars
        owner_width = max(15, max_owner + 2)
        
        # Print formatted table
        print("\nAvailable Tenable.io Scans:")
        separator = "-" * (name_width + owner_width + 15)  # Total width including spacing
        print(separator)
        print(f"{'Scan Name':<{name_width}} {'Owner':<{owner_width}} {'ID':<10}")
        print(separator)
        
        # Print each scan with proper formatting
        for scan in scans:
            name_truncated = str(scan['name'])[:name_width-3] + '...' if len(str(scan['name'])) > name_width else str(scan['name'])
            print(f"{name_truncated:<{name_width}} {str(scan['owner']):<{owner_width}} {str(scan['id']):<10}")
        print(separator)
        print()
            
    except Exception as e:
        print(f"\nError retrieving scans: {str(e)}")
        if 'raw_scans' in locals():
            print("\nDebug - Raw scan data:")
            pprint.pprint(raw_scans)










