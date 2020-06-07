# Copyright (c) 2017 Adafruit Industries
# Author: Tony DiCola & James DeVito
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess
import datetime
import psutil
#battery level
import struct
import smbus
import sys
import time


def readVoltage(bus):

     address = 0x36
     read = bus.read_word_data(address, 2)
     swapped = struct.unpack("<H", struct.pack(">H", read))[0]
     voltage = swapped * 1.25 /1000/16
     return voltage


def readCapacity(bus):

     address = 0x36
     read = bus.read_word_data(address, 4)
     swapped = struct.unpack("<H", struct.pack(">H", read))[0]
     capacity = swapped/256/113*100
     return capacity


bus = smbus.SMBus(1) # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

#while True:

 #print "******************"
 #print "Voltage:%5.2fV" % readVoltage(bus)

 #print "Battery:%5i%%" % readCapacity(bus)

 #if readCapacity(bus) == 100:

         #print "Battery FULL"

 #if readCapacity(bus) < 20:


         #print "Battery LOW"
 #print "******************"
 #time.sleep(2)
#prevent the program from being run  times
'''cmd = r'ps aux|grep stats.py'
MemUsage = subprocess.check_output(cmd, shell = True )
ss=str(MemUsage).split('\\n')
is_exist=[]
f=open(r'/home/pi/Desktop/log.txt','w')
for i in ss:
    is_exist.append('python3' in i and 'stats.py' in i and 'thonny' not in i)
    f.writelines(str(is_exist)+'\n')
    f.writelines(str(i)+'\n')
f.close()
if is_exist.count(True)<3:'''
while True:
    # Raspberry Pi pin configuration:
    #RST = None     # on the PiOLED this pin isnt used
    RST = 25
    # Note the following are only used with SPI:
    #DC = 23
    DC = 24
    SPI_PORT = 0
    SPI_DEVICE = 0

    # Beaglebone Black pin configuration:
    # RST = 'P9_12'
    # Note the following are only used with SPI:
    # DC = 'P9_15'
    # SPI_PORT = 1
    # SPI_DEVICE = 0

    # 128x32 display with hardware I2C:
    #disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

    # 128x64 display with hardware I2C:
    #disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

    # Note you can change the I2C address by passing an i2c_address parameter like:
    # disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3C)

    # Alternatively you can specify an explicit I2C bus number, for example
    # with the 128x32 display you would use:
    # disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, i2c_bus=2)

    # 128x32 display with hardware SPI:
    # disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

    # 128x64 display with hardware SPI:
    disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, dc=DC, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=8000000))

    # Alternatively you can specify a software SPI implementation by providing
    # digital GPIO pin numbers for all the required display pins.  For example
    # on a Raspberry Pi with the 128x32 display you might use:
    # disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST, dc=DC, sclk=18, din=25, cs=22)

    # Initialize library.
    disp.begin()

    # Clear display.
    disp.clear()
    disp.display()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = -2
    top = padding
    bottom = height-padding
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0


    # Load default font.
    font = ImageFont.truetype('/home/pi/Desktop/111.TTF',11)

    # Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
    # Some other nice fonts to try: http://www.dafont.com/bitmap.php
    # font = ImageFont.truetype('Minecraftia.ttf', 8)

    while True:
        #disp.clear()
        #disp.display()
        # disp.clear()
        # disp.display()
        # Draw a black filled box to clear the image.
        draw.rectangle((0,0,width,height), outline=0, fill=0)

        # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
        #cmd = "hostname -I | cut -d\' \' -f1"
        #IP = subprocess.check_output(cmd, shell = True )
        startTime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(psutil.boot_time()))
        endTime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        startTime= datetime.datetime.strptime(startTime,'%Y-%m-%d %H:%M:%S')
        endTime= datetime.datetime.strptime(endTime,"%Y-%m-%d %H:%M:%S")
        hours=round((endTime- startTime).seconds/3600,2)
        hour=str(int(str(hours).split('.')[0])+int((endTime- startTime).days*24))
        min=str(hours).split('.')[1]
        min=str(round(float('0.'+min)*60,2))
        cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
        CPU = subprocess.check_output(cmd, shell = True )
        #***************************************
        cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
        MemUsage = subprocess.check_output(cmd, shell = True )
        #*****************************
        cmd = r'cat /sys/class/thermal/thermal_zone0/temp'
        CpuTemp = subprocess.check_output(cmd, shell = True )
        
        cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
        Disk = subprocess.check_output(cmd, shell = True )
        try:
            voltage=str(round(float(readVoltage(bus)),2))
            cap=str(int(readCapacity(bus)))
        except Exception as e:
            voltage = 'AC'
            cap = ' '

        # Write two lines of text.

        #draw.text((x, top),       "IP: " + str(IP)[2:15],  font=font, fill=255)
        if voltage!='AC':
            draw.text((x, top),       "UpT: " + hour+'h'+min+'m'+'            '+'batt:', font=font, fill=255)
        else:
            draw.text((x, top),       "UpT: " + hour+'h'+min+'m'+'      '+'power:', font=font, fill=255)
        #draw.text((x, top),       "UpT: " + hour+'h'+min+'m'+'            ', font=font, fill=255)
        '''draw.text((x, top+17),     str(CPU)[2:16]+'       '+voltage+'V', font=font, fill=255)
        draw.text((x, top+35),    'CpuTemp: '+str(CpuTemp)[2:4]+'.'+str(CpuTemp)[5:6]+'℃'+'    '+cap+'%',  font=font, fill=255)
        draw.text((x, top+55),    str(Disk)[2:18],  font=font, fill=255)
        draw.text((x, top+55),     str(MemUsage), font=font, fill=255)'''
        if voltage!='AC':
            draw.text((x, top+13),     str(CPU)[2:16]+'        '+voltage+'V', font=font, fill=255)
        else:
            draw.text((x,top+13),     str(CPU)[2:16]+'       '+'AC',font=font, fill=255)
        #draw.text((x,top+13),     str(CPU)[2:16],font=font, fill=255)
        if voltage!='AC':
            draw.text((x, top+26),    'CpuTemp: '+str(CpuTemp)[2:4]+'.'+str(CpuTemp)[5:6]+'℃'+'    '+cap+'%',  font=font, fill=255)
        else:
            draw.text((x, top+26),    'CpuTemp: '+str(CpuTemp)[2:4]+'.'+str(CpuTemp)[5:6]+'℃',  font=font, fill=255)
        #draw.text((x, top+26),    'CpuTemp: '+str(CpuTemp)[2:4]+'.'+str(CpuTemp)[5:6]+'℃'+'    '+cap+'%',  font=font, fill=255)
        #draw.text((x, top+26),    'CpuTemp: '+str(CpuTemp)[2:4]+'.'+str(CpuTemp)[5:6]+'℃',  font=font, fill=255)
        draw.text((x, top+39),    str(Disk)[2:18],  font=font, fill=255)
        draw.text((x, top+55),     str(MemUsage)[2:-1], font=font, fill=255)
        # Display image.
        disp.image(image)
        disp.display()
        time.sleep(0.1)
