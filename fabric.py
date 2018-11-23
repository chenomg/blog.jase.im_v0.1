#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import paramiko
ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('i.jase.im', 26630, 'root', 'yjbtGApfGLPT', timeout=5)
channel = ssh.invoke_shell()
channel.invoke_shell('ls')
channel.invoke_shell('cd /home/chenomg/www/blog.jase.im_v0.1/jase_im/')
channel.invoke_shell('ls')
# si, so, err = ssh.exec_command('cd /home/chenomg/www/blog.jase.im_v0.1/jase_im/ && ls')
# print(so.read().decode('utf-8'))
# step2 = ssh.exec_command('rm -r collected_static')
# step3 = ssh.exec_command('python3 manage.py collectstatic')
# si, so, err = ssh.exec_command('ls')
# print(so.read().decode('utf-8'))
# print(step2)
# print(step3)
