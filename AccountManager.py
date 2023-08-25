print("Loading FSE Accountant \n")

#import needed modules
import os
import json
import csv

#global variables to go here
userSettings = {}
userKey = ""
readerKey = ""
managedAccountName = ""
ownedAirports = []
ownedAircraft = []

#functions to go here
def configJsonCreate():
    userKey = input("Please enter the Access Key of your FSE account from the Home -> Data feeds section.")
    readerKey = input("Please enter the Access Key of the account you would like to be managed from the Home -> Data feeds section")
    managedAccountName = input("Please enter the name of the account to be managed as it appears in the Home -> Data feeds section")
    airports = input("Please enter the list of owned airports, seperated by a comma. Example: EGCC,EGKK,EGLL")
    ownedAirports = airports.split(",")
    aircraft = input("Please enter the registrations of any owned aircraft seperated by a comma. Example: G-FYUK,EI-KHJ,N8766")
    ownedAircraft = aircraft.split(",")
    userSettings = {
        "User Key":userKey,
        "Reader Key":readerKey,
        "Managed Account":managedAccountName,
        "Owned Airports":ownedAirports,
        "Owned Aircraft":ownedAircraft
    }
    configFile = open("config.json","w")
    json.dump(userSettings,configFile)
    configFile.close()
    print("Config file created succesfully.")

def configJsonImport():
    #referencing the global values defined at the top of program
        global userKey
        global readerKey
        global managedAccountName
        global ownedAircraft
        global ownedAirports
    #importing the config file and assigning the saved values to the global values
        configFile = open("config.json")
        settings = json.load(configFile)
        userKey = settings["User Key"]
        readerKey = settings["Reader Key"]  
        managedAccountName = settings["Managed Account"]
        ownedAircraft = settings["Owned Aircraft"]
        ownedAirports = settings["Owned Airports"]
        print("Config imported succesfully")
        configFile.close() 

def configJsonModify():
    print("Function not finished.")

 
#main code, prompts, and input to go here

#initial boot checks for prior settings, if file doesn't exist one is created
if os.path.exists("config.json"):
    print("Prior config found. Importing data.")
    configJsonImport()

else:
    x = input("No config found, would you like to create one now? Y / N")