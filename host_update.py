#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import paramiko
import json
"""
(host.key) config sample
{
    "hostname": "hostname/ip",
    "port": port,
    "username": "username",
    "password": "password",
    "dir": "django_dir"
}
"""
KEY_FILE = 'host.key'


def get_config(key_file=KEY_FILE):
    with open(key_file, 'r') as k:
        _key = json.load(fp=k)
    return _key


config = get_config()
cmd = 'cd ' + config['dir'] + ';\
    rm -r collected_static;\
    git fetch;\
    git reset --hard origin/master;\
    git pull;\
    pip3 install -r requirements.txt;\
    python3 manage.py makemigrations;\
    python3 manage.py migrate;\
    python3 manage.py collectstatic;\
    service apache2 restart'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.load_system_host_keys()
client.connect(config['hostname'], config['port'], config['username'], config['password'])
stdin, stdout, stderr = client.exec_command(cmd)
print(stdout.read().decode('utf-8'))
print('Process Done')
