# nlt-github
*nlt-github is an open source project which makes sure that you don't have to leave your beloved terminal to upload a new project in Github.*

![](https://img.shields.io/badge/python-3-blue.svg?style=for-the-badge&logo=python)
[![Gitter](https://img.shields.io/gitter/room/:user/:repo.svg?style=for-the-badge)](https://gitter.im/kwoc_19/nlt-github?utm_source=share-link&utm_medium=link&utm_campaign=share-link)

## Installation
`$ git clone https://github.com/dibyasonu/nlt-github.git`

`$ pip install --editable .`

## Steps
1. **First we need to create a user. Creating a user creates a personal access token and stores the data to access the token
locally**

    `$ nlt config --adduser`

2. **We add files like gitignore, LICENSE and README. (Optional)**

    `$ nlt add --gitignore` shows templates list for different languages, the user can select any no of languages and accordingly
gitignore is addded to your project folder.

    `$ nlt add --license` shows templates list for different LICENSE, the user can select any one and 
LICENSE file is generated and accordingly addded to your project folder.

    `$ nlt add --readme` adds a README.md to your project.

3. **We create a Repo in your github account. We upload the project from the terminal.**

    `$ nlt create-remote `
Prompts for the **username** and the details like **repo name** and **Description** of the repo. It creates a repo 
according to given details, and adds its remote address to the origin referrence to the local project.

    `$ nlt create-remote --privy`
 It does the above task but the repo created is a **private** repo. 

    Now you can push the project simply by  `git push --all`


## Usage

`$ nlt --help`
```
Usage: nlt [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  add            Add required files.
  config         Configure Users.
  create-remote  create a new repo in Github and add remote origin to the local project.
```

#### Add required files

`$ nlt add --help`

```
Usage: nlt add [OPTIONS]

  Add required files

Options:
  --license    Add license templates from the list to your project.
  --gitignore  Add gitignore template from the list to your Project.
  --readme     Addd README to your project.
```

#### Configure Users

`$ nlt config --help`

```
Usage: nlt config [OPTIONS]

  Configure Users

Options:
  --adduser    Creates a personal access token in github and stores them locally.
  --deluser    Remove created personal access token from github and locally.
  --showusers  Show added users.
```

#### Create repo

`$ nlt create-remote --help`

```
Usage: nlt create-remote [OPTIONS]

Options:
  --username TEXT  provide username in whose account the new repo is to be created.
  --privy          create a private repository if used.
```
