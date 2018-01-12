from bluetooth import *
import RPi.GPIO as GPIO        #calling for header file which helps in using GPIOs of PI
import picamera
import datetime
import time
import threading
import BMP280 as BMP280
import logging

sensor = BMP280.BMP280()

camera = picamera.PiCamera()
camera.resolution = (1280, 720)

socket=BluetoothSocket( RFCOMM )
 
bd_addr = "98:D3:31:50:3A:86" #Rocketbox Address
port = 1

threads = []

f = open("box-recording.txt","w") 

initAlt = sensor.read_altitude() 

def altworker():
	"""thread worker function"""
	for i in range(0, 960):
		f.write('======================================================================\n')
		f.write('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + '\n')
		f.write('Temp = {0:0.2f} *C'.format(sensor.read_temperature()) + '\n')
		f.write('Pressure = {0:0.2f} Pa'.format(sensor.read_pressure()) + '\n')
		f.write('Altitude = {0:0.2f} m'.format(sensor.read_altitude()) + '\n')
		f.write('Sealevel Pressure = {0:0.2f} Pa'.format(sensor.read_sealevel_pressure()) + '\n')
		f.write('======================================================================\n\n')
		socket.send('Altitude = {0:0.2f} m'.format(sensor.read_altitude()) + '\n')
		time.sleep(1)
	#Save/Close the file
	f.close()
	socket.send("Finished Altitude Data Recording!\n")
	return 

def vidworker():
	"""thread worker function"""
	camera.start_recording('bt-activated-video.h264')
	camera.wait_recording(960)
	camera.stop_recording()
	socket.send("Finished Video Recording")
	return 
 
sock.connect((bd_addr, port))
print "Connected to: ",bd_addr

socket.send("RSV BT Connection Established")

try:
	while 1:
		data = socket.recv(1024)
		print "Received: %s" % data

		if (data == "1"):    #if '0' is sent from the Android App, turn OFF the LED
			t = threading.Thread(target=vidworker)
			threads.append(t)
			t.start()
			socket.send("Video Recording Started")
		if (data == "2"):    #if '1' is sent from the Android App, turn OFF the LED
			t2 = threading.Thread(target=altworker)
			threads.append(t2)
			t2.start()
			socket.send("Data Recording Started")
		if (data == "q"):
			print ("Quit")
			socket.send("Quit Command Received")
			break

except KeyboardInterrupt:  
		# here you put any code you want to run before the program   
		# exits when you press CTRL+C  
	camera.close()
	f.close()
	print "\n", counter # print value of counter

finally:  
	GPIO.cleanup() # this ensures a clean exit     