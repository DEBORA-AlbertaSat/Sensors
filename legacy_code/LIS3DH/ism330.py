#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  setuplsm6ds.py
#  
#  Copyright 2022  <debora22@raspberrypi>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
# 
# import time
# import board
# import busio
# 
# from adafruit_lsm6ds.ism330dhcx import ISM330DHCX
# 
# i2c = board.I2C()
# sensor = ISM330DHCX(i2c)
# 
# 
# while True:
#     print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (sensor.acceleration))
#     print("Gyro X:%.2f, Y: %.2f, Z: %.2f degrees/s" % (sensor.gyro))
#     print("")
#     time.sleep(1.0) 

import time
import board
#import busio

from adafruit_lsm6ds.ism330dhcx import ISM330DHCX

i2c = board.I2C()
time.sleep(0.5)
# sensor = ISM330DHCX(i2c, address = 0x6a)


g = 1

# x,y,z = sensor.acceleration
# a,b,c = sensor.gyro

while True:
    sensor = ISM330DHCX(i2c, 0x6a)
    x,y,z = sensor.acceleration
    a,b,c = sensor.gyro
    print(g)
    print("Acceleration:",x,y,z, "m/s^2")
    print("Gyro X:",a,b,c, "degrees/s")
    print("")
    g = g + 1
    time.sleep(0.5)


