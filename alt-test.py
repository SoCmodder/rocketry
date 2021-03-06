#!/usr/bin/python
# Author: Mitch Miller <socmodder@gmail.com>
import logging
import BMP280 as BMP280
import time
import datetime

logging.basicConfig(level=logging.DEBUG)

sensor = BMP280.BMP280()

# Open File
f = open("test-data.txt","w") 

for i in range(0, 30):
	f.write('======================================================================\n')
	f.write('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + '\n')
	f.write('Temp = {0:0.2f} *C'.format(sensor.read_temperature()) + '\n')
	f.write('Pressure = {0:0.2f} Pa'.format(sensor.read_pressure()) + '\n')
	f.write('Altitude = {0:0.2f} m'.format(sensor.read_altitude()) + '\n')
	f.write('Sealevel Pressure = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure()) + '\n')
	f.write('======================================================================\n\n')
	time.sleep(1)

#Save/Close the file
f.close()