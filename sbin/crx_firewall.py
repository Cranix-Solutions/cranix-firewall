#!/usr/bin/python3
# Copyright 2024 Dipl. Ing. Peter Varkoly <pvarkoly@cephalix.eu>. All rights reserved.
import json
import subprocess
import sys
import cranixconfig

CRANIX_FW_CONFIG="/etc/cranix-firewall.conf"
config = json.load(open(CRANIX_FW_CONFIG))

def log_debug(msg):
    if cranixconfig.CRANIX_DEBUG == "yes":
        print(msg)


def start_fw():

    for pre in config.get("pre_rules", []):
        log_debug(pre)
        subprocess.run(pre, shell=True)

    # Open ports to devices
    for zone, ip_ports in config.get("open_ports", {}).items():
        device = config['devices'][zone]
        for port in ip_ports:
            num, prot = port.split("/")
            command = f"/usr/sbin/iptables -A INPUT -i {device} -p {prot} --dport {num} -j ACCEPT"
            log_debug(command)
            subprocess.run(command, shell=True)

    # Open ports to devices from ip adressess
    for zone, ip_ports in config.get("open_ports_with_ip", {}).items():
        device = config['devices'][zone]
        for ip_range, ports in ip_ports.items():
            for port in ports:
                num, prot = port.split("/")
                command = f"/usr/sbin/iptables -A INPUT -i {device} -p {prot} --dport {num} -s {ip_range} -j ACCEPT"
                log_debug(command)
                subprocess.run(command, shell=True)

    # NAT rules
    for zone, nat_rules in config.get("nat_rules", {}).items():
        device = config['devices'][zone]
        for rule in nat_rules:
            command = f"/usr/sbin/iptables -t nat -A POSTROUTING  -s {rule['source']} -o {device}"
            if rule.get('proto',"all") != "all" and rule.get('proto',"all") != "":
                command += f" -p {rule['proto']}"
            if rule.get('dest',"0/0") != "0/0" and rule.get('dest',"") != "" :
                command += f" -d {rule['dest']}"
            to_source=rule.get('to_source',"")
            if to_source == "":
                to_source = cranixconfig.CRANIX_SERVER_EXT_IP
            command += f" -j SNAT --to-source {to_source}"
            log_debug(command)
            subprocess.run(command, shell=True)
            command = f"/usr/sbin/iptables -A FORWARD -s {rule['source']} -o {device} -j ACCEPT"
            if rule.get('dest',"") != "":
                command += f" -d {rule['dest']}"
            log_debug(command)
            subprocess.run(command, shell=True)

    # Port forwarding rules.
    for zone, port_forward_rules in config.get("port_forward_rules", {}).items():
        device = config['devices'][zone]
        for rule in port_forward_rules:
            command = f"/usr/sbin/iptables -t nat -A PREROUTING -p {rule['proto']} -i {device} --dport {rule['dport']} -j DNAT --to-destination {rule['to_ip']}:{rule['to_port']}"
            log_debug(command)
            subprocess.run(command, shell=True)
            command = f"/usr/sbin/iptables -A INPUT -p {rule['proto']} -d {rule['to_ip']} --dport {rule['to_port']} -j ACCEPT"
            log_debug(command)
            subprocess.run(command, shell=True)
            command = f"/usr/sbin/iptables -A FORWARD -p {rule['proto']} -d {rule['to_ip']} --dport {rule['to_port']} -j ACCEPT"
            log_debug(command)
            subprocess.run(command, shell=True)

    for post in config.get("post_rules", []):
        log_debug(post)
        subprocess.run(post, shell=True)

def open_fw():
    for cmd in config.get("open_rules", []):
        subprocess.run(cmd, shell=True)

def fw_status():
    subprocess.run("/usr/sbin/iptables -vnL", shell=True)
    subprocess.run("/usr/sbin/iptables -t nat -vnL", shell=True)

if len(sys.argv) == 1 or sys.argv[1] == "start":
    start_fw()
elif sys.argv[1] == "stop":
    open_fw()
elif sys.argv[1] == "open":
    open_fw()
elif sys.argv[1] == "status":
    fw_status()
else:
    print("Unknown parameter. Valid parameters are start, stop, open, status")
