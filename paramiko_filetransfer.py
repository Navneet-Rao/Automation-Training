#! /usr/bin/python3
import paramiko

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect( hostname='192.168.126.131',password='Navneet@123',username='navneet')
sftp=ssh.open_sftp()
sftp.put('/home/navneet/file.py','/home/navneet/Ansible-Training/group/abc.yml')
sftp.close()
ssh.close()
