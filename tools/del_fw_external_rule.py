#!/usr/bin/python3
# Copyright 2024 Dipl. Ing. Peter Varkoly <pvarkoly@cephalix.eu>. All rights reserved.
import json
import os
import sys

CRANIX_FW_CONFIG="/etc/cranix-firewall.conf"

#Read new services and ports from standard input
rule=json.loads(input(""))
config = json.load(open(CRANIX_FW_CONFIG))
if rule in config["nat_rules"]["external"]:
    config["nat_rules"]["external"].remove(rule)
    with open(CRANIX_FW_CONFIG,"w") as f:
        json.dump(config, f, indent=True)
    os.system("/usr/sbin/crx_firewall.py")
elif "to_source" in rule:
    del rule["to_source"]
    if rule in config["nat_rules"]["external"]:
        config["nat_rules"]["external"].remove(rule)
        with open(CRANIX_FW_CONFIG,"w") as f:
            json.dump(config, f, indent=True)
        os.system("/usr/sbin/crx_firewall.py")
