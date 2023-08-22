#import needed modules
import os
import json
import csv

#global variables to go here

#functions to go here

#main code, prompts, and input to go here

if os.path.exists("config.json"):
    print("Prior config found. Importing data.")
else:
    print("No config found, would you like to create one now?")