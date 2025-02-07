#!/usr/bin/python3
import os
import json
import sys

CRANIX_FW_CONFIG="/etc/cranix-firewall.conf"
config = json.load(open(CRANIX_FW_CONFIG))
device = config['devices']['internal']

for room in json.load(os.popen('/usr/sbin/crx_api.sh GET rooms/all')):
    try:
        ip_range=f"{room['startIP']}/{room['netMask']}"
        command = f"/usr/sbin/iptables -A INPUT -i {device} -s {ip_range} -j ACCEPT"
        os.system(command)
    except:
        print("open_rooms error", room)

