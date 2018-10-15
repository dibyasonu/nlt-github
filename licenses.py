from __future__ import print_function, unicode_literals
import os
import click
import datetime
import requests
import click
import json
from subprocess import call, STDOUT


def getRequestsAsJSON(fromURL):
    return requests.get(fromURL).json()

def getLicenseKey(lics, choice):

    return [k for k, v in lics.items() if v == choice][0]


def replacePlaceholders(licenseText, licenseIdentifier, authorName, licenseYear):

    if licenseIdentifier == 'gpl-3.0' or licenseIdentifier == 'agpl-3.0':
        programName = click.prompt("\nEnter program name")
        desc = click.prompt("\nEnter one line to give a brief idea of what the program does")
        return licenseText.replace('<year>', str(licenseYear)).replace('<name of author>', authorName).replace('<program>', programName).replace("<one line to give the program's name and a brief idea of what it does.>", (programName + ' ' + desc))

    elif licenseIdentifier == 'apache-2.0':
        return licenseText.replace('[yyyy]', str(licenseYear)).replace('[name of copyright owner]', authorName)

    elif licenseIdentifier == 'gpl-2.0':
        return licenseText.replace('Copyright (C) year name of author', ('Copyright (C) ' + str(licenseYear) + ' ' + authorName))

    elif licenseIdentifier == 'lgpl-2.1':
        libraryName = click.prompt("\nEnter library name")
        desc = click.prompt("\nEnter one line to give a brief idea of what the library does")
        return licenseText.replace('<year>', str(licenseYear)).replace('<name of author>', authorName).replace("<one line to give the library's name and a brief idea of what it does.>", (libraryName + ' ' + desc))
    
    else:
        return licenseText.replace('[year]', str(licenseYear)).replace('[fullname]', authorName)



def createLicense(srcURL, lKey):

    licenseBody = getRequestsAsJSON(srcURL + '/' + lKey)['body']
    name = click.prompt("\nEnter your name")
    year = click.prompt("\nEnter the year(Press enter to use the current year)", show_default = False, default = datetime.datetime.now().year)
    licenseBody = replacePlaceholders(licenseBody, lKey, name, year)
    licenseFile = open('LICENSE', 'w')
    licenseFile.write(licenseBody)


def generateLicense(licenseURL, licenses, chosen):

    click.clear()
    chosenLicenseKey = getLicenseKey(licenses, chosen)
    createLicense(licenseURL, chosenLicenseKey)
    click.secho("\nCreated LICENSE file based on the %s in the current directory.\n" %
          chosen, fg = "green", bold = True)
