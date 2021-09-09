import subprocess,sys,time,logging,os
import nmapper.nmapper

menu_str = "What would you like to launch today? \n (Please enter a number) \n 1 - nmapper \n 2 - Coming Soon! \n 3 - Exit"

#func for the swissmenu
def swissmenu() :
    in_menu = True
    while in_menu:
        print(menu_str)
        moduleload = input ("> ")
        if moduleload == "1" :
            nmapper.nmapper.nmapper()
        elif moduleload == "2" :
            print("There is no module to load. Come back later!")
        elif moduleload == "3" : 
            print("Goodbye!")
            in_menu = False
        elif moduleload != ["1","2","3"] :
            print("Invalid value!")

swissmenu()
