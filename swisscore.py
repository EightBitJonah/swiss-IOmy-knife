import subprocess,time,logging,os,pprint
import nmapper.nmapper
import mescans.mescans
import sys
import importlib.util

# Import the Database class
spec = importlib.util.spec_from_file_location("database", os.path.join(os.path.dirname(os.path.abspath(__file__)), "db", "database.py"))
database = importlib.util.module_from_spec(spec)
spec.loader.exec_module(database)
Database = database.Database

menu_str = """What would you like to launch today? 
(Please enter a number)
1 - nmapper 
2 - mescans 
3 - help (coming soon)
4 - API Key Management
5 - Exit"""

def manage_api_keys():
    db = Database('swissknife.db')
    while True:
        print("\nAPI Key Management")
        print("1 - Update Tenable.io Keys")
        print("2 - Show Current API Keys")
        print("3 - Purge API Keys")
        print("4 - Back to Main Menu")
        
        choice = input("> ")
        if choice == "1":
            access_key = input("Enter Tenable.io Access Key: ")
            secret_key = input("Enter Tenable.io Secret Key: ")
            db.store_api_key('tenable', access_key, secret_key)
            print("API keys updated successfully!")
        elif choice == "2":
            keys = db.get_api_key('tenable')
            if keys:
                access_key, secret_key = keys
                print("\nCurrent Tenable.io Keys:")
                print(f"Access Key: {access_key}")
                print(f"Secret Key: {'*' * len(secret_key)}")
            else:
                print("No API keys set for Tenable.io")
        elif choice == "3":
            confirm = input("Are you sure you want to purge the API keys? (yes/no): ")
            if confirm.lower() == 'yes':
                db.cursor.execute('DELETE FROM api_keys WHERE service = ?', ('tenable',))
                db.connection.commit()
                print("API keys have been purged successfully!")
            else:
                print("Purge cancelled.")
        elif choice == "4":
            break
    db.close()

def swissmenu():
    in_menu = True
    while in_menu:
        print(menu_str)
        moduleload = input("> ")
        if moduleload == "1":
            nmapper.nmapper.nmapper()
        elif moduleload == "2":
            mescans.mescans.mescans()
        elif moduleload == "3": 
            print("Under construction!")
        elif moduleload == "4":
            manage_api_keys()
        elif moduleload == "5":
            print("Goodbye!")
            in_menu = False
        else:
            print("Invalid value!")

swissmenu()