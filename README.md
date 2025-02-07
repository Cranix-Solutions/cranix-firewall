# cranix-firewall
Firewall configurator for CRANIX/CEPHALIX

cranix-firewall is a simple firewall configurations tool which kann controll the access to the **CRANIX/CEPHALIX** server based on a json configurations file: `/etc/cranix-firewall.conf`. This configuration file has following sections:

**open_rules**: This is an array of commands which will be executed when the firewall will be opened.

**pre_rules**: This is an array of commands which will be executed when the firewall will be started.

**devices**: Here you can assign network cards to zones. Normaly two zones should exist "external" and "internal". This assigment will be made by first start of cranix-firewall according to the network configuration. All arbitary zones can be defined. In the different rule sections the rules will be ordered in this zones.

**open_ports**: In this section the ports which have to been opened in a zone can be defined.

**open_ports_with_ip**: In this section the ports which have to been opened in a zone can be defined as in open_ports. In this section the acces can be reduced for ip adresses or ip address areas.

**nat_rules**: In this section NAT rules can be defined by MASQUERAD or SNAT depending on if to_source will be given.

**port_forward_rules**: Port forwarding rules can be defined for the zones.

**post_rules**: An array of commands which will be executed after all rules were set.

The firewall will be started by executing `/usr/sbin/crx_firewall.py`. This program accept three command line parameters:

**start** Starting the firewall. All rules will be set.

**open** **stop** Stops the firewall. The commands in section **open_rules** will be executed: All rules will be removed and the default policy will be set to ACCEPT in all chains (INPUT FORWARD OUTPUT).

**status** List all firewall rules including the package counts.

The standard configuration after installing cranix-firewall:

```
{
     "open_rules": [
         "/usr/sbin/iptables -t mangle -F",
         "/usr/sbin/iptables -t nat -F",
         "/usr/sbin/iptables -F",
         "/usr/sbin/iptables -P INPUT ACCEPT",
         "/usr/sbin/iptables -P FORWARD ACCEPT",
         "/usr/sbin/iptables -P OUTPUT ACCEPT"
    ],
    "pre_rules": [
        "/usr/sbin/iptables -t mangle -F",
        "/usr/sbin/iptables -t nat -F",
        "/usr/sbin/iptables -F",
        "/usr/sbin/iptables -P INPUT DROP",
        "/usr/sbin/iptables -P FORWARD DROP",
        "/usr/sbin/iptables -P OUTPUT ACCEPT",
        "/usr/sbin/iptables -I INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT",
        "/usr/sbin/iptables -I FORWARD -m state --state RELATED,ESTABLISHED -j ACCEPT",
        "/usr/sbin/iptables -I INPUT -i lo -j ACCEPT",
        "/usr/sbin/iptables -I FORWARD -o lo -j ACCEPT",
        "/usr/sbin/iptables -I FORWARD -i lo -j ACCEPT"
    ],
    "devices": {
        "external": "#EXT_DEV#",
        "internal": "#INT_DEV#"
    },
    "open_ports": {
        "external": ["ssh/tcp", "https/tcp"],
        "internal": [ ]
    },
    "open_ports_with_ip": {
        "external": { },
        "internal": { }
    },
    "nat_rules": {
        "external": [
            {
                "proto": "",
                "source": "#CRANIX_SERVER_NET#",
                "dest": "",
                "to_source": "#CRANIX_SERVER_EXT_IP#"
            }
        ],
        "internal": []
    },
    "port_forward_rules": {
        "external": [],
        "internal": []
    },
    "post_rules": [
        "/usr/share/cranix/tools/wait-for-api.sh",
        "/usr/share/cranix/tools/firewall/open_rooms.py",
        "/usr/sbin/crx_manage_room_access.py --all --set_defaults",
        "test -e /usr/share/cranix/tools/custom/fw-post-start.sh && /usr/share/cranix/tools/custom/fw-post-start.sh"
    ]
}
```

You can edit this configurtation file. After each change you have to start cranix-firewall again. This file will be modified by cranix-api if you defines new incomming outgoing or remote access rules. 
* The incomming rules take place in open_ports.external section.
* The outgoing will be writte in nat_rules.external section.
* The remote access rules you can find in port_forward_rules.external section.

The rules for room access controll will be set dynamically by the `crx_manage_room_access.py` command and will not be written in the firewall configuration. Please note that after all start of the firewall the actual room access control rules will be removed and the default states will be set in all dynamically controllable room.

In the /usr/share/cranix/tools/firewall/ you can find some tools to modify the static firewall configuration. All programms reads the values from the standard input.

```
add_fw_external_rule.py del_fw_external_rule.py
add_fw_open_rules.py del_fw_open_rules.py
add_fw_remote_access_rule.py del_fw_remote_access_rule.py
add_fw_incomming.py del_fw_incomming.py
set_fw_incomming.py
add_fw_pre_rules.py del_fw_pre_rules.py
convert_firewalld_to_cranix.py
open_rooms.py**
```

