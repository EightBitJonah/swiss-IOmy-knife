import subprocess,sys,time,logging,os

print("Loading SwissCore . . . ")
 
def swissmenu() :
        print("What would you like to launch today? \n (Please enter a number) \n 1 - nmapper \n 2 - Coming Soon! \n 3 - Exit")
        moduleload = input ("> ")
        while True :

                if moduleload == "1" :
                        import nmapper.nmapper 
                elif moduleload == "2" :
                        print("There is no module to load. Come back later!")
                        swissmenu()
                elif moduleload == "3" : 
                        print("Goodbye!")
                        time.sleep(3)
                        exit()
                elif moduleload != ["1","2","3"] :
                        swissmenu()
swissmenu()
