# NLT
*NLT is an open source project which makes sure that you don't have to leave your beloved terminal to upload a new project in Github.*

![](https://img.shields.io/badge/python-3-blue.svg?style=for-the-badge&logo=python)

## Installation
`$ git clone https://github.com/dibyasonu/NLT.git`

`$ pip install --editable .`

## Usage
```
Usage: nlt [OPTIONS] COMMAND [ARGS]...
Options:
  --help  Show this message and exit.

Commands:
  config         Configure Users
  create-remote  create a project on Github and add remote origin
```

#### Configure Users

```
Usage: nlt config [OPTIONS]
Options:
  --adduser    Add a user and their credentials
  --deluser    Remove user and their credentials
  --showusers  Show users 
  --help       Show this message and exit.
```

#### Create repo

```
Usage: nlt create-remote [OPTIONS]
Options:
  --username TEXT  username to push
  --privy          create a private repository if used
  --help           Show this message and exit.
```
