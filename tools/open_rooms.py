#!/usr/bin/python3
import os
import json
import sys
import cranixconfig
import ipaddress

CRANIX_FW_CONFIG="/etc/cranix-firewall.conf"
config = json.load(open(CRANIX_FW_CONFIG))
interfaces = os.popen("ip -o -f inet addr show").read().strip().split('\n')

def get_interface_of_ip(ip_str):
    ip = ipaddress.ip_address(ip_str)
    for interface in interfaces:
        parts = interface.split()
        iface_name = parts[1]
        iface_ip = parts[3]
        network = ipaddress.ip_network(iface_ip, strict=False)
        if ip in network:
            return iface_name

main_dev = get_interface_of_ip(cranixconfig.CRANIX_SERVER)

for room in json.load(os.popen('/usr/sbin/crx_api.sh GET rooms/all')):
    try:
        device=get_interface_of_ip(room['startIP'])
        ip_range=f"{room['startIP']}/{room['netMask']}"
        command = f"/usr/sbin/iptables -A INPUT -i {device} -s {ip_range} -j ACCEPT"
        os.system(command)
        if device != main_dev:
            command = f"/usr/sbin/iptables -A FORWARD -i {device} -s {ip_range} -d {cranixconfig.CRANIX_SERVER_NET} -j ACCEPT"
            os.system(command)
            command = f"/usr/sbin/iptables -A FORWARD -o {device} -d {ip_range} -s {cranixconfig.CRANIX_SERVER_NET} -j ACCEPT"
            os.system(command)
    except:
        print("open_rooms error", room)

