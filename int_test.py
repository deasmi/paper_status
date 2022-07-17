#!/usr/bin/python3

import sys
import os
import platform
import netifaces
from pprint import pprint

for interface in ["wlan0","usb0","tailscale0"]:
    gws=netifaces.gateways()
    default=gws['default'][netifaces.AF_INET][1]

    int_addrs = netifaces.ifaddresses(interface)
    if netifaces.AF_INET in int_addrs:
        ipv4 = int_addrs[netifaces.AF_INET]
        for address in ipv4:
            if interface == default:
                print(address['addr'],'-',interface,'*')
            else:
                print(address['addr'],'-',interface)
                
