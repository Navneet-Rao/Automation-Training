#! /home/navneet/automation/myenv/bin/python

from netmiko import ConnectHandler
import re
connect = ConnectHandler(
    device_type='cisco_ios',
    host='192.168.62.3',
    username='admin',
    password='admin')

output=connect.send_command("sh ip int brief")


connect.enable()

config=["interface loopback0",
    "ip address 1.1.1.1 255.255.255.255",
    "no shutdown"]

print(connect.send_config_set(config))

connect.disconnect()



