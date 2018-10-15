from __future__ import print_function, unicode_literals
import os
import click # handling ImportError from this would be redundant
import datetime

try:
    import requests
except ImportError:
    # print("\33[32m" + "\nInstalling required dependencies, \n\n")
    click.secho("\nInstalling required dependencies, \n\n", fg = "green")
    os.system('pip install requests')
    import requests


try:
    import click
except ImportError:
    # print("\33[32m" + "\nInstalling required dependencies, \n\n")
    click.secho("\nInstalling required dependencies, \n\n", fg = "green")
    os.system('pip install click')
    import click

import json
from subprocess import call, STDOUT

try:
    from pick import pick
except ImportError:
    click.secho("\nInstalling required dependencies, \n\n", fg = 'green')
    if(os.name == 'nt'):
        os.system('pip install windows-curses pick') # pick depends on curses, workaround for windows
    else:
        os.system('pip install pick')
    from pick import pick


def getRequestsAsJSON(fromURL):

    return requests.get(fromURL).json()


def getLicenseChoice(lics):

    promptMessage = 'Choose a license: '
    title = promptMessage
    options = list(lics.values())
    option, index = pick(options, title, indicator = '=>', default_index = 0)
    # user selection is stored in option, which is the index'th element in options = licenses
    return option


def getLicenseKey(lics, choice):

    return [k for k, v in lics.items() if v == choice][0]


def wantsLicense():

    choice, index = pick(['Yes', 'No'], 'Do you want to add a license?', indicator = "=>", default_index = 0)

    if(choice == 'Yes'):
        return True
    else:
        return False


def createLicense(srcURL, lKey):

    licenseBody = getRequestsAsJSON(srcURL + '/' + lKey)['body']
    # name = input("\nEnter your name: ")
    # year = input("\nEnter the year: ")
    name = click.prompt("\nEnter your name")
    year = click.prompt("\nEnter the year(Press enter to use the current year)", show_default = False, default = datetime.datetime.now().year)
    licenseBody = licenseBody.replace('[year]', str(year)).replace('[fullname]', name)

    licenseFile = open('LICENSE', 'w')
    licenseFile.write(licenseBody)


def isGitRepository():

    if (call(["git", "branch"], stderr = STDOUT, stdout = open(os.devnull, 'w')) != 0):
        return False
    else:
        return True


def generateLicense():

    click.clear()
    licenseURL = 'https://api.github.com/licenses'
    response = getRequestsAsJSON(licenseURL)

    licenses = {}
    for i in response:
        licenses[i['key']] = i['name']

    chosenLicense = getLicenseChoice(licenses)
    chosenLicenseKey = getLicenseKey(licenses, chosenLicense)
    createLicense(licenseURL, chosenLicenseKey)
    click.secho("\nCreated LICENSE file based on the %s in the current directory.\n" %
          chosenLicense, fg = "green", bold = True)


if __name__ == '__main__':

    if(not isGitRepository()):
        click.echo("\nNot a git repository, exiting.")
        quit()

    generateLicense()
