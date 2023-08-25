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
    ownedAirports.sort()
    aircraft = input("Please enter the registrations of any owned aircraft seperated by a comma. Example: G-FYUK,EI-KHJ,N8766")
    ownedAircraft = aircraft.split(",")
    ownedAircraft.sort()
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

def fubar():
    print("You are having a bad day if you see this message. Go to the Github page for this program and raise an issue. - Ashley-Zorah")
    print("Program will now self close after 3 seconds.")
    time.sleep(3)
    os._exit()

def configJsonImport():
    configFile = open("config.json")
    settings = json.load(configFile)
    userKey = settings["User Key"]
    readerKey = settings["Reader Key"]  
    managedAccountName = settings["Managed Account"]
    ownedAircraft = settings["Owned Aircraft"]
    ownedAircraft.sort()
    ownedAirports = settings["Owned Airports"]
    ownedAirports.sort()
    print("Config imported succesfully")
    configFile.close()
    return userKey,readerKey,managedAccountName,ownedAircraft,ownedAirports

def configJsonModify(configField,configValue,modifier="remove"):
    configFile = open("config.json")
    settings = json.load(configFile)
    configFile.close()
    if type(configValue) == list:
        temp = settings[configField]
        if modifier == "remove":
            for value in configValue:
                temp.remove(value)
        elif modifier == "add":
            for value in configValue:
                temp.append(value)
        else:
            fubar()
        temp.sort()
        settings[configField] = temp
    else:
        settings[configField] = configValue
    configFile = open("config.json","w")
    json.dump(settings,configFile)
    configFile.close()

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
    userKey,readerKey,managedAccountName,ownedAircraft,ownedAirports = configJsonImport()
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

while validConfig == False:
    if validConfigMessage == "Invalid User Key":
        print("Invalid User Key in config file. Please verify and enter the correct User Access Key. \n")
        newKey = input()
        configJsonModify("User Key",newKey)
        userKey,readerKey,managedAccountName,ownedAircraft,ownedAirports = configJsonImport()
        validConfig, validConfigMessage = configJsonValidate(userKey,readerKey,managedAccountName)
    elif validConfigMessage == "Invalid Account Key":
        print("Invalid key for the account to be managed. Please verify and enter the correct Access Key for the account to be managed. \n")
        newKey = input()
        configJsonModify("Reader Key",newKey)
        userKey,readerKey,managedAccountName,ownedAircraft,ownedAirports = configJsonImport()
        validConfig, validConfigMessage = configJsonValidate(userKey,readerKey,managedAccountName)
    elif validConfigMessage == "Invalid Account Key":
        print("Invalid key for the account to be managed. Please verify and enter the correct Access Key for the account to be managed. \n")
        newKey = input()
        configJsonModify("Reader Key",newKey)
        userKey,readerKey,managedAccountName,ownedAircraft,ownedAirports = configJsonImport()
        validConfig, validConfigMessage = configJsonValidate(userKey,readerKey,managedAccountName)
    else:
        fubar()
