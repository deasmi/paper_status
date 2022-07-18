#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sys
import os
import platform
import netifaces

picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
print(libdir)
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd2in13b_V3
import time
from PIL import Image,ImageDraw,ImageFont,ImageColor
import traceback
from uptime import uptime
from uptime import boottime
import subprocess
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd2in13b_V3 Demo")
    
    epd = epd2in13b_V3.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
#    time.sleep(1)
    
    # Drawing on the image
    logging.info("Drawing")    
    font20 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font14 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 14)
    font10 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 10)
    
    # Drawing on the Horizontal image
    logging.info("1.Drawing on the Horizontal image...") 
    HBlackimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126
    HRYimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126  ryimage: red or yellow image  
    drawblack = ImageDraw.Draw(HBlackimage)
    drawry = ImageDraw.Draw(HRYimage)

    drawblack.text((10,0), platform.node(), font = font20, fill = 0)

    gws=netifaces.gateways()
    if netifaces.AF_INET in gws['default']:
        default=gws['default'][netifaces.AF_INET][1]
    else:
        default=''

    icount=0 # How many lines have we printed so far
    offset=17 # How far from the top should the first line be
    lineheight=14 # How high are the linesl


    # Iterate over few interfaces we are likely to want to know about
    for interface in ["wlan0","usb0","tailscale0"]:
        if interface == "wlan0":
            output = subprocess.run(["/sbin/iwgetid -r"], shell = True, check = False)
            if output.returncode == 0:
                ssid = output.decode().rstrip()
                label = "ssid: %s" % ssid
            else:
                label = "ssid: Not Connected"
            drawblack.text((10,(icount*lineheight+offset)), label ,font = font14, fill = 0)
            icount+=1
        int_addrs = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in int_addrs: # Check if we have any AF_INET (ipv4) addresses
            ipv4 = int_addrs[netifaces.AF_INET] # Get all addresses
            for address in ipv4: # For each one print a label to the screen
                label = "%s - %s" % (address['addr'],interface)
                if interface == default: # Check for default and make red
                    drawry.text((10,(icount*lineheight+offset)), label ,font = font14, fill = 0)
                else:
                    drawblack.text((10,(icount*lineheight+offset)), label ,font = font14, fill = 0)
                icount+=1 # Increment number of lines printed

    # Put boottime at bottom right
    boottime = boottime().strftime("B:%Y-%m-%d %H%M")
    w, h = font10.getsize(boottime)
    x = epd.height - w - 1
    y = epd.width - h - 1
    drawblack.text((x,y),boottime, font = font10, fill = 0)

    # Put update time in bottom left
    now = datetime.now().strftime("N:%Y-%m-%d %H%M")
    w, h = font10.getsize(boottime)
    x = 1
    y = epd.width - h - 1
    drawblack.text((x,y),now, font = font10, fill = 0)


    # Display the output
    epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
   
    
    logging.info("Goto Sleep...")
    epd.sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13b_V3.epdconfig.module_exit()
    exit()
