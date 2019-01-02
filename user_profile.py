import sys
import os
import click
import datetime
import requests
import click
import json
from prettytable import PrettyTable

def display_repo(data,username,all):
    if all:
        if username in data.keys():
            payload = {'type':'owner','per_page':100}
            url='https://api.github.com/user/repos'
            headers={"Authorization": "token "+data[username][0]}
            response=requests.get(url,headers=headers,params=payload)
        else:
            click.secho('User not configured can not view private repos. Add users by running "nlt config --adduser".\n', fg = "red", bold = True)
            sys.exit(0)
    else:
        payload = {'per_page':100}
        url='https://api.github.com/users/'+username+'/repos'
        response=requests.get(url,payload)
    if response.status_code == 200:
        response=response.json()
        t = PrettyTable(['Repo','url','* star'])
        i=1
        for repo in response:
            t.add_row([repo["name"],repo["html_url"],repo["stargazers_count"]])

        click.secho(t.get_string(sortby="* star",reversesort=True))
    else:
        click.secho("Internal error occured.", bold=True, fg='red')
        sys.exit(0)

def display_profile(data,username,all):
    if all:
        if username in data.keys():
            url='https://api.github.com/user'
            headers={"Authorization": "token "+data[username][0]}
            response=requests.get(url,headers=headers)
        else:
            click.secho('User not configured can not view private repos. Add users by running "nlt config --adduser".\n', fg = "red", bold = True)
            sys.exit(0)
    else:
        url='https://api.github.com/users/'+username
        response=requests.get(url)
    if response.status_code == 200:
        response=response.json()
        click.secho(response['name']+" ("+username+")", bold=True, fg='yellow')
        if(response['email']):
            click.secho("Location: "+str(response['email']))
        if(response['company']):
            click.secho("Company: "+str(response['company']))
        if(response['location']):
            click.secho("Location: "+str(response['location']))
        if(response['bio']):
            click.secho("Bio: "+response['bio'])
        click.secho("Public repos: "+str(response['public_repos']))
        if all:
            click.secho("Private repos: "+str(response['total_private_repos']))
        click.secho("Followers: "+str(response['followers'])+" || Following: "+str(response['following']))
        url='https://api.github.com/users/'+username+'/events/public'
        response=requests.get(url)
        if response.status_code == 200:
            response=response.json()
            if len(response)>0:
                click.secho('last public activity: '+response[0]['created_at'])
        option=click.prompt("Press l to view repos else anything else to stop")
        if(option.lower()=='l'):
            if all:
                display_repo(data,username,True)
            else:
                display_repo(data,username,False)
        else:
            sys.exit(0)

    else:
        click.secho("Internal error occured.", bold=True, fg='red')
        sys.exit(0)		
