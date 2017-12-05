#!/usr/bin/python
# Author: Mitch Miller <socmodder@gmail.com>
import logging
import BMP280 as BMP280

logging.basicConfig(level=logging.DEBUG)

sensor = BMP280.BMP280()

# Open File
f = open(“data.txt”,”w”) 

f.write('Temp = {0:0.2f} *C'.format(sensor.read_temperature()))
f.write('Pressure = {0:0.2f} Pa'.format(sensor.read_pressure()))
f.write('Altitude = {0:0.2f} m'.format(sensor.read_altitude()))
f.write('Sealevel Pressure = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure()))

#Save/Close the file
f.close()