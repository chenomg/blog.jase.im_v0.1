#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import paramiko
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.load_system_host_keys()
client.connect(host, port, user, password)
stdin, stdout, stderr = client.exec_command('cd %project_path%;rm -r collected_static;git fetch;git reset --hard origin/master;git pull;ls -l;python3 manage.py collectstatic;ls -l;service apache2 restart')
