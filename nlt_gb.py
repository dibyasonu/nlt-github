import os
import getpass
import subprocess
import requests
import click
import json
import colorama
import licenses
from pick import pick

@click.group()
def cli():
	pass
def read_data():
	osuser = getpass.getuser()
	
	if os.name == 'nt':
		pat = os.path.join("C:", os.sep, "Users", osuser)
	else:
		pat = os.path.join("/", "home", osuser)
	
	nltpath = os.path.join(pat, '.nlt')
	if not os.path.isfile(nltpath):
		with open(nltpath, 'w')as file:
			data={}
			json.dump(data,file)
	else:
		with open(nltpath, 'r')as file:
			data=json.load(file)

	return [data,pat]
	
def execute(com):
	proc=subprocess.Popen(com,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	stdout_value = proc.communicate()[0]
	print(stdout_value.decode("utf-8"))

@cli.command('create-remote',short_help='create a project on Github and add remote origin ')
@click.option('--username',prompt=True,help='username to push')
@click.option('--privy',is_flag=bool,default=False,help="create a private repository if used")
def push_remote(username,privy):
	data=read_data()[0]
	if username in data.keys():
		proname=click.prompt('Please enter the Project name')
		desc=click.prompt('A short description of the repository.')
		headers={"Authorization": "token "+data[username][0]}
		proname = proname.strip().replace(' ', '-') #sanitization
		
		payload={"name": proname,"description": desc,"private": privy,"has_issues": True,"has_projects": True,"has_wiki": True}
		
		response=requests.post('https://api.github.com/user/repos', headers=headers, data=json.dumps(payload))
		
		if response.status_code == 201:
			repo_url = response.json()['clone_url']
			click.secho('Repo created succesfully\n',bold=True,fg='green')
			click.secho(f'\nYour repository name is {proname}',bold=True,fg='green')
			click.secho(f'\nand it is at {repo_url}\n',bold=True,fg='green')
			command="git remote add origin "+repo_url
			execute(command)
			click.secho('Remote added succesfully',bold=True,fg='green')

		else:
			click.secho(str(response.json()),bold=True,fg='red')
	else:
		click.secho('user not found',bold=True,fg='red')
		click.secho('\nAdd a user using "nlt config --adduser"\n',bold=True,fg='green')

@cli.command('config',help="Configure Users")
@click.option('--admin',is_flag=bool,default=False,help="Add a default global user for your machine")
@click.option('--adduser',is_flag=bool,default=False,help="Add a user and their credentials")
@click.option('--deluser',is_flag=bool,default=False,help="Remove user and their credentials")
@click.option('--showusers',is_flag=bool,default=False,help="Show users and token status")
def user_config(admin,adduser,deluser,showusers):
	data=read_data()[0]
	pat=read_data()[1]
	if admin:
		if bool(data):
			pass
			#work to do	
		else:
			click.secho('No users added. Add users by running "nlt config --adduser"',bold=True,fg='red')
	if adduser:
		user_name=click.prompt('Please enter your Github user name')
		password=click.prompt('Enter the password',hide_input=True)
		if user_name in data.keys():
			click.secho('user exists',bold=True,fg='red')
			#checks whether token status is ok	output exists(enhancment)
			#token status is not ok ask to delete and create a new token;addusr(enhancment)	
		else:
			payload='{"scopes": ["admin:public_key", "admin:repo_hook", "delete_repo", "repo", "user"], "note": "NLT"}'
			response=requests.post('https://api.github.com/authorizations',data=payload,auth=(user_name, password))
			if response.status_code==201:
				data[user_name]=[response.json()['token'],response.json()['url']]

			nltpath = os.path.join(pat, '.nlt')
			with open(nltpath, 'w+') as file:
				json.dump(data,file)
			click.secho('user added succesfully',bold=True,fg='green')	
			
			# ADD CONDITION TO CHECK IF TOKEN EXISTS
			#checks if user don't exist locally but token is in github import it and add user(enhancment)<not possible>
			#so delete it and add another token
		
	if deluser:
		user_name=click.prompt('Please enter your Github user name')
		password=click.prompt('Enter the password',hide_input=True)
		if user_name in data.keys():
			response=requests.delete(data[user_name][1], auth=(user_name, password))
			if response.status_code==204:
				data.pop(user_name)
				with open(pat+'.nlt', 'w+')as file:
					json.dump(data,file)
				click.secho('user deleted succesfully',bold=True,fg='green')
			else:
				click.secho('Enter the right credentials',bold=True,fg='red')
		else:
			click.secho('user not found',bold=True,fg='red')

	if showusers:
		users=[x for x in data]
		if len(users):
			for i in users:
				click.secho(i,bold=True,fg='blue')
		else:
			click.secho('No users added. Add users by running "nlt config --adduser"',bold=True,fg='red')
		#checks users as well as their status and generate the status	

@cli.command('add',help="Add required files")
@click.option('--license',is_flag=bool,default=False,help="Add license to your project")
@click.option('--gitignore',is_flag=bool,default=False,help="Add gitignore to your Project")
@click.option('--readme',is_flag=bool,default=False,help="Addd README to your project")
def add(license, gitignore, readme):
	if license:

		click.clear()
		licenseURL = 'https://api.github.com/licenses'
		GETResponse = licenses.getRequestsAsJSON(licenseURL)

		licensesDict = {}
		for i in GETResponse:
			licensesDict[i['key']] = i['name']

		promptMessage = 'Choose a license: '
		title = promptMessage
		options = list(licensesDict.values())
		chosenLicense, index = pick(options, title, indicator = '=>', default_index = 0)
		# user selection is stored in chosenLicense, which is the index'th element in options = licenses
		licenses.generateLicense(licenseURL, licensesDict, chosenLicense)

	if gitignore:
		with open('.gitignore', 'w+') as file:
			pass
	if readme:			
		with open('README.md', 'w+') as file:
			pass	
	
  	click.pause(info = 'Press any key to view git status ...')
	click.clear()
	execute('git status')

if __name__ == '__main__':
	cli()
