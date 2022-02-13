import subprocess,sys,time,logging,os,pprint
import nmapper.nmapper
import mescans.mescans

menu_str = "What would you like to launch today? \n (Please enter a number) \n 1 - nmapper \n 2 - mescans \n 3 - help (coming soon) \n 4 - Exit"

#func for the swissmenu
def swissmenu() :
    in_menu = True
    while in_menu:
        print(menu_str)
        moduleload = input ("> ")
        if moduleload == "1" :
            nmapper.nmapper.nmapper()
        elif moduleload == "2" :
            mescans.mescans.mescans()
        elif moduleload == "3" : 
            print("Under construction!")
        elif moduleload == "4" :
            print("Goodbye!")
            in_menu = False
        elif moduleload != ["1","2","3","4"] :
            print("Invalid value!")

swissmenu()