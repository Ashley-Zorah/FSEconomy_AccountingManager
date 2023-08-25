print("Loading FSE Accountant \n")

#import needed modules
import os
import json
import csv
import time

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

def configJsonImport(userKey,readerKey,managedAccountName,ownedAircraft,ownedAirports):
    configFile = open("config.json")
    settings = json.load(configFile)
    userKey = settings["User Key"]
    readerKey = settings["Reader Key"]  
    managedAccountName = settings["Managed Account"]
    ownedAircraft = settings["Owned Aircraft"]
    ownedAirports = settings["Owned Airports"]
    print("Config imported succesfully")
    configFile.close() 

def configJsonModify(configField,configValue):
    print("Function not finished.")

def configJsonValidate(userKey,readerKey,managedAccountName):
    validation = True
    validationMessage = ""
    if userKey == "" or len(userKey) != 16:
        validation = False
        validationMessage = "Invalid User Key"
    elif readerKey == "" or len(readerKey) != 16:
        validation = False#
        validationMessage = "Invalid Account Key"
    elif managedAccountName == "":
        validation = False
        validationMessage = "Managed Account Name is empty"
    return validation, validationMessage

 
#main code, prompts, and input to go here
validInput = False

#initial boot checks for prior settings, if file doesn't exist one is created
if os.path.exists("config.json"):
    print("Prior config found. Importing data.")
    configJsonImport(userKey,readerKey,managedAccountName,ownedAircraft,ownedAirports)
    validConfig = configJsonValidate(userKey,readerKey,managedAccountName)
else:
    while validInput == False:
        x = input("No config found, would you like to create one now? Y / N \n")
        if x.upper() == "N":
            validInput = True
            print("Unable to proceed without config. FSE Accountant will now close.")
            time.sleep(2)
            os._exit()
        elif x.upper() =="Y":
            validInput = True
            configJsonCreate()
            validConfig, validConfigMessage = configJsonValidate(userKey,readerKey,managedAccountName)

if validConfig == False:
