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
    "password": "password"
}
"""
KEY_FILE = 'host.key'
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


def get_config(key_file=KEY_FILE):
    with open(key_file, 'r') as k:
        _key = json.load(fp=k)
    return _key


key = get_config()
cmd = 'cd ' + PROJECT_DIR + ';rm -r collected_static;git fetch;git reset --hard origin/master;git pull;python3 manage.py collectstatic;service apache2 restart'

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.load_system_host_keys()
client.connect(key.hostname, key.port, key.username, key.password)
stdin, stdout, stderr = client.exec_command(cmd)
print(stdout.read().decode('utf-8'))
