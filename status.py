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

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd2in13b_V3 Demo")
    
    epd = epd2in13b_V3.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
    time.sleep(1)
    
    # Drawing on the image
    logging.info("Drawing")    
    font20 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font14 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 14)
    
    # Drawing on the Horizontal image
    logging.info("1.Drawing on the Horizontal image...") 
    HBlackimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126
    HRYimage = Image.new('1', (epd.height, epd.width), 255)  # 298*126  ryimage: red or yellow image  
    drawblack = ImageDraw.Draw(HBlackimage)
    drawry = ImageDraw.Draw(HRYimage)

    # drawblack.text((10, 0), 'hello world', font = font20, fill = 0)
    # drawblack.text((10, 20), '2.13inch e-Paper bc', font = font20, fill = 0)
    # drawblack.text((120, 0), u'微雪电子', font = font20, fill = 0)    
    # drawblack.line((20, 50, 70, 100), fill = 0)
    # drawblack.line((70, 50, 20, 100), fill = 0)
    # drawblack.rectangle((20, 50, 70, 100), outline = 0)    
    # drawry.line((165, 50, 165, 100), fill = 0)
    # drawry.line((140, 75, 190, 75), fill = 0)
    # drawry.arc((140, 50, 190, 100), 0, 360, fill = 0)
    # drawry.rectangle((80, 50, 130, 100), fill = 0)
    # drawry.chord((85, 55, 125, 95), 0, 360, fill =1)

    drawblack.text((10,0), platform.node(), font = font20, fill = 0)

    gws=netifaces.gateways()
    default=gws['default'][netifaces.AF_INET][1]

    icount=0
    offset=17
    lineheight=14
    for interface in ["wlan0","usb0","tailscale0"]:
        int_addrs = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in int_addrs:
            ipv4 = int_addrs[netifaces.AF_INET]
            for address in ipv4:
                label = "%s - %s" % (address['addr'],interface)
                if interface == default:
                    drawry.text((10,(icount*lineheight+offset)), label ,font = font14, fill = 0)
                else:
                    drawblack.text((10,(icount*lineheight+offset)), label ,font = font14, fill = 0)
                icount+=1

            
    
    
    epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRYimage))
    time.sleep(2)
    
    
    logging.info("Goto Sleep...")
    epd.sleep()
        
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd2in13b_V3.epdconfig.module_exit()
    exit()
