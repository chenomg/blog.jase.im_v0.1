#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import paramiko
import json

# 用于存放服务器登陆信息的文件, 格式如下
"""
(KEY_FILE: host.key) config sample
{
    "hostname": "hostname/ip",
    "port": port,
    "username": "username",
    "password": "password",
    "dir": "django_project_dir"
}
"""
KEY_FILE = 'host.key'


# 获取服务器数据
def get_config(key_file=KEY_FILE):
    with open(key_file, 'r') as k:
        _key = json.load(fp=k)
    return _key


config = get_config()
# 远程执行自动部署代码
cmd = 'cd ' + config['dir'] + ';\
    rm -r collected_static;\
    git fetch;\
    git reset --hard origin/master;\
    git pull;\
    cd ..;\
    pip3 install -r requirements.txt;\
    cd jase_im;\
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
