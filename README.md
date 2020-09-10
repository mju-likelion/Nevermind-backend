# nevermind-backend

## General Server Info

- OS: Ubuntu 18.04 LTS
- Cloud Instance: AWS EC2
- IPv4: 3.128.164.186

## Setup

### OS setup
1. sudo apt-get update
2. sudo apt-get install python3
3. sudo apt-get install python3-pip
4. sudo apt-get install build-essential libssl-dev libffi-dev python-dev libmysqlclient-dev
5. sudo apt-get install mysql-server mysql-client
6. sudo pip3 install virtualenv
7. sudp pip3 install uwsgi

### virtualenv setup after clone
(Run from project root directory)
1. python3 -m virtualenv venv
2. source venv/bin/activate
3. pip3 install -r requirements.txt
4. cd nevermind
5. python3 manage.py makemigrations
6. python3 manage.py migrate
7. deactivate