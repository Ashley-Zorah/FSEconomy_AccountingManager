print("Loading FSE Accountant \n")

#import needed modules
import os
import json
import csv
import time
import requests
import numpy as np
import pandas as pd

#global variables to go here
userSettings = {}
userKey = ""
readerKey = ""
managedAccountName = ""
ownedAirports = []
ownedAircraft = []
apiURL = "https://server.fseconomy.net/data?userkey={}&format=csv&query=payments&search=monthyear&readaccesskey={}&month={}&year={}"
monthLookup = {
    "january":1,
    "february":2,
    "march":3,
    "april":4,
    "may":5,
    "june":6,
    "july":7,
    "august":8,
    "september":9,
    "october":10,
    "november":11,
    "december":12,
}
doContinue = False
validConfig = False
validConfigMessage = ""
financeData = {}

#functions to go here
def configJsonCreate():
    userKey = input("Please enter the Access Key of your FSE account from the Home -> Data feeds section. \n")
    readerKey = input("Please enter the Access Key of the account you would like to be managed from the Home -> Data feeds section \n")
    managedAccountName = input("Please enter the name of the account to be managed as it appears in the Home -> Data feeds section \n")
    airports = input("Please enter the list of owned airports, seperated by a comma. Example: EGCC,EGKK,EGLL \n")
    ownedAirports = airports.split(",")
    ownedAirports.sort()
    aircraft = input("Please enter the registrations of any owned aircraft seperated by a comma. Example: G-FYUK,EI-KHJ,N8766 \n")
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
    print("Config file created succesfully. \n")

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
    print("Config imported succesfully \n")
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
        validation = False
        validationMessage = "Invalid Account Key"
    elif managedAccountName == "":
        validation = False
        validationMessage = "Managed Account Name is empty"
    return validation, validationMessage

def recordCleanup(financeData):
    recordsToRemove = []
    for record in financeData:
        if financeData[record]["Account From"] == managedAccountName and financeData[record]["Account To"] == managedAccountName:
            recordsToRemove.append(record)
    for key in recordsToRemove:
        financeData.pop(key)

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

# This should really be a stuck look till both conditions are met. To investigate after processing of data is written
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
while doContinue == False:
    print(""" The name of the managed account is {}.
        Your ownend aircraft are {}
        Your owned airports are {}
        """.format(managedAccountName,ownedAircraft,ownedAirports))
    x = input("Is this correct? \n")
    if x.upper() == "N":
        y = input("""Please select one of the following values to modify:
                1 - Name of the Managed Account
                2 - The list of owned aircraft
                3 - The list of owned airports
                """)
        if y == 1:
            newValue = input("Please enter the name of the account to be managed as it appears in the Home -> Data feeds section \n")
            configJsonModify("Reader Key",newKey)
            userKey,readerKey,managedAccountName,ownedAircraft,ownedAirports = configJsonImport()
            validConfig, validConfigMessage = configJsonValidate(userKey,readerKey,managedAccountName)
        elif y == 2:
            addRemove = input("Do you wish to add or remove aircraft from this list? {}".format(ownedAircraft))
            temp = input("Please enter all aircraft registrations to be added or removed, separated by a comma. Example: G-FYUK,EIKHJ,N8766 \n")
            aircraftList = temp.split(",")
            configJsonModify("Owned Aircraft",aircraftList)
        elif y == 3:
            addRemove = input("Do you wish to add or remove aircraft from this list? {}".format(ownedAircraft))
            temp = input("Please enter all aircraft registrations to be added or removed, separated by a comma. Example: EGCC,EGKK,EGLL \n")
            airportList = temp.split(",")
            configJsonModify("Owned Airports",airportList)
    else:
        doContinue = True

x = input("Please enter the name of the month you want to get the data for. \n")
requestedMonth = monthLookup[x.lower()]
requestedYear = input("Please enter the year you want to get the data for. \n")
requestURL = apiURL.format(userKey,readerKey,requestedMonth,requestedYear)

print("Fetching data, Please wait.")
# Maybe merge import and clean into one single function? Leaving seperate as is for now to better understand the flow of the program
response = requests.request("GET",requestURL)

responseTXT = response.text

response = open("response.csv","w")
response.write(responseTXT)
response.close()

with open("response.csv") as responseCSV:
    responseImport = csv.DictReader(responseCSV)
    for row in responseImport:
        paymentID = row["Id"]
        financeData[paymentID] = {
            "Account From":row["From"],
            "Account To":row["To"],
            "Payment Amount":row["Amount"],
            "Payment Reason":row["Reason"],
            "Payment FBO":row["Fbo"],
            "Payment Location":row["Location"],
            "Aircraft Registration":row["Aircraft"],
            "Misc Data":row["Comment"]
        }

# Removing transaction going from managed account to the same account
recordCleanup(financeData)
