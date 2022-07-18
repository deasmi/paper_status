#!/usr/bin/env python3

import sys
import os
import platform
import netifaces
from pprint import pprint

for interface in ["wlan0","usb0","tailscale0"]:
    gws=netifaces.gateways()
    if netifaces.AF_INET in gws['default']:
        default=gws['default'][netifaces.AF_INET][1]
    else:
        default=''

    print(default)
    
    int_addrs = netifaces.ifaddresses(interface)
    if netifaces.AF_INET in int_addrs:
        ipv4 = int_addrs[netifaces.AF_INET]
        if interface == "wlan0":
            output = subprocess.run(["/sbin/iwgetid -r"], shell = True, check = False)
            if output.returncode == 0:
                ssid = output.decode().rstrip()
                label = "ssid: %s" % ssid
            else:
                label = "ssid: Not Connected"
            print(label)

        for address in ipv4:
            if interface == default:
                print(address['addr'],'-',interface,'*')
            else:
                print(address['addr'],'-',interface)
                
