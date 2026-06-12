import paramiko
username="navneet"
password="Navneet@123"
command="uptime"

with open("/home/navneet/automation/hosts.txt") as f:
    hosts=f.read().splitlines()
   

for i in hosts:
    try:
         c=paramiko.SSHClient()
         c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
         c.connect(i,username=username,password=password)
         inpu,output,error=c.exec_command(command)
         print(output.read())
    finally:     
         c.close()
