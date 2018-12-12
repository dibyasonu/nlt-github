import os
import sys
import getpass
import subprocess
import requests
import click
import json
import colorama
from cryptography.fernet import Fernet
import licenses
from pick import pick
from pick import Picker

@click.group()
def cli():
	pass

def encrypt(data):
 	cipher_key = Fernet.generate_key()
 	cipher = Fernet(cipher_key)
 	interim = json.dumps(data)
 	end_string = str.encode(interim)
 	encrypted_text = cipher.encrypt(end_string)
 	return encrypted_text+cipher_key


def decrypt(data):
	cipher_key = data[-44:]
	data = data[:-44]
	cipher = Fernet(cipher_key)
	decrypted_text = cipher.decrypt(data)
	interim = decrypted_text.decode()
	end_string = json.loads(interim)
	return end_string

def file_handler(*argv):
	osuser = getpass.getuser()
	if os.name == 'nt':
		pat = os.path.join("C:", os.sep, "Users", osuser)
	elif sys.platform == 'darwin':
		pat = os.path.join("/","Users",osuser)
	else:
		pat = os.path.join("/", "home", osuser)
	nltpath = os.path.join(pat,'.nlt')
	if not os.path.isfile(nltpath):
			with open(nltpath, 'wb')as file:
				if(not len(argv)):
					data = {}
				else:
					data = argv[0]
				data = encrypt(data)
				file.write(data)
				data = decrypt(data)
	else:
		if(not len(argv)):
			with open(nltpath, 'rb') as file:
				data = file.read()
				data = decrypt(data)
		else:
			with open(nltpath,'wb') as file:
				data = argv[0]
				data = encrypt(data)
				file.write(data)
				data = decrypt(data)

	return data


def execute(com):
	proc=subprocess.Popen(com,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
	stdout_value = proc.communicate()[0]
	print(stdout_value.decode("utf-8"))


def go_back(picker):
	return None, -1


@cli.command('create-remote',short_help='create a new repo in Github and add remote origin to the local project.')
@click.option('--username',prompt=True,help='provide username in whose account the new repo is to be created.')
@click.option('--privy',is_flag=bool,default=False,help="create a private repository if used.")
def push_remote(username,privy):
	data=file_handler()

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
# @click.option('--admin',is_flag=bool,default=False,help="Add a default global user for your machine")
@click.option('--adduser',is_flag=bool,default=False,help="Creates a personal access token in github and stores them locally.")
@click.option('--deluser',is_flag=bool,default=False,help="Remove created personal access token from github and locally.")
@click.option('--showusers',is_flag=bool,default=False,help="Show added users.")
def user_config(adduser,deluser,showusers):
	data=file_handler()
	# if admin:

	# 	if bool(data):
	# 		pass
	# 		#work to do
	# 	else:
	# 		click.secho('No users added. Add users by running "nlt config --adduser"',bold=True,fg='red')

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

			file_handler(data)
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

				file_handler(data)
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
@click.option('--license',is_flag=bool,default=False,help="Add license templates from the list to your project.")
@click.option('--gitignore',is_flag=bool,default=False,help="Add gitignore template from the list to your Project.")
@click.option('--readme',is_flag=bool,default=False,help="Addd README to your project.")
def add(license, gitignore, readme):

	if license:
		click.clear()
		licenseURL = 'https://api.github.com/licenses'
		GETResponse = licenses.getRequestsAsJSON(licenseURL)
		licensesDict = {}

		for i in GETResponse:
			licensesDict[i['key']] = i['name']
		promptMessage = 'Choose a license or press s to stop'
		title = promptMessage
		options = list(licensesDict.values())
		picker = Picker(options, title, indicator = '=>', default_index = 0)
		picker.register_custom_handler(ord('s'),  go_back)
		chosenLicense, index = picker.start()
		# user selection is stored in chosenLicense, which is the index'th element in options = licenses
		if index != -1:
			licenses.generateLicense(licenseURL, licensesDict, chosenLicense)
		else:
			sys.exit(0)

	if gitignore:
		url = "https://api.github.com/repos/github/gitignore/contents/"
		r = requests.get(url)

		if r.status_code==200:
			x = r.json()
		else:
			click.secho("Internal error occured.", bold=True, fg='red')
			sys.exit(0)
		ignores = [{"name" : item['name'], "url" : item['download_url']} for item in x if item['type']=='file' and ".gitignore" in item['name']]
		promptMessage = 'Choose a gitignore \n(press SPACE to mark, ENTER to continue, s to stop):'
		title = promptMessage
		options = [item['name'] for item in ignores]
		picker = Picker(options, title, multi_select=True, min_selection_count=1)
		picker.register_custom_handler(ord('s'),  go_back)
		selected = picker.start()

		if type(selected) == list:
			d_urls = [ignores[item[1]]['url'] for item in selected]
		else:
			sys.exit(0)
		sep = "\n"+("#" * 40)+"\n"
		str_write = ''.join(["".join(sep+requests.get(item).text+sep) for item in d_urls])

		with open('.gitignore', 'a+') as file:
			file.write(str_write)
		click.secho("gitignore templates added succesfully.\n", fg = "green", bold = True)

	if readme:			
		with open('README.md', 'w+') as file:
			pass	


if __name__ == '__main__':
	cli()