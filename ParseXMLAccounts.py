'''
Author: Matthew Stephenson
Created on: July 23, 2015
'''

import xml.etree.ElementTree as ET
import datetime
import re
import os
from sys import exit

class Account(object):
    first_name = ""
    last_name = ""
    birthdate = None
    profession = ""
    street = ""
    city = ""
    state = ""
    zipcode = 0

    def __init__(self, fname, lname, bdate, prof, street, city, state, zipcode):
        self.first_name = fname
        self.last_name = lname
        self.birthdate = datetime.datetime.strptime(bdate, "%m/%d/%Y")
        self.profession = prof
        self.street = street
        self.city = city
        self.state = state
        self.zipcode = zipcode

    def __repr__(self):
        output =  "Name: " + self.first_name + " " + self.last_name + "\n"
        output += "Profession: " + self.profession + "\n"
        output += "Address: " + self.getAddress() + "\n"
        output += "Age: " + str(self.getAge()) + "\n"
        return output

    def __str__(self, *args):
        return repr(self)

    def getAge(self):
        if not self.birthdate:
            return -1

        today = datetime.date.today()
        return today.year - ( self.birthdate.year + ((today.month, today.day) < (self.birthdate.month, self.birthdate.day)) )

    def getAddress(self):
        return self.street + " " + self.city + ", " + self.state + " " + str(self.zipcode)

    def getFullName(self):
        return self.first_name + " " + self.last_name

    def getFirstName(self):
        return self.first_name

    def getLastName(self):
        return self.last_name

def exportAccounts():
    try:
        XMLFile = ET.parse("inputDataFile.xml")
    except:
        print("ERROR: Missing input XML file.\nPlease place inputDataFile.xml in the same directory as this Python script.\n")
        exit()

    root = XMLFile.getroot()
    accounts = []

    for a in root:
        # Separate full name into first and last names
        name = re.search("(?P<first_name>\w+) (?P<last_name>\w+)", a.attrib['name'])
        fname = name.group('first_name')
        lname = name.group('last_name')

        # Birthdate in MM/DD/YYYY form
        bdate = a.find("Birthdate").text

        prof = a.find("Profession").text

        # Get the address tag and get data
        address = a.find("Address")
        street = address.find("Street").text
        city = address.find ("City").text
        state = address.find("State").text
        zipcode = int(address.find("Zip").text)

        # Add current account to the list of accounts
        accounts.append(Account(fname, lname, bdate, prof, street, city, state, zipcode))

    accounts.sort(key=lambda x: x.last_name)

    # Check if the Year folder exists. If not, create it.
    if not os.path.exists("./Year/"):
        os.makedirs("./Year/")

    # Export individual files as well as the sorted file.
    with open("./Year/sortedByLastName.txt", 'w') as sortedFile:
        for a in accounts:
            path = "./Year/" + str(a.birthdate.year) + "/"

            if not os.path.exists(path):
                os.makedirs(path)

            path += a.getLastName() + ".txt"
            with open(path, 'w') as individualFile:
                individualFile.write(repr(a) + "\n")
                sortedFile.write(repr(a) + "\n")

exportAccounts()
