import picamera
import bluetooth
import RPi.GPIO as GPIO        #calling for header file which helps in using GPIOs of PI
import datetime
import time
import threading
import BMP280 as BMP280
import logging

logging.basicConfig(level=logging.DEBUG)

sensor = BMP280.BMP280()

LED=21

GPIO.setmode(GPIO.BCM)     #programming the GPIO by BCM pin numbers. (like PIN40 as GPIO21)
GPIO.setwarnings(False)
GPIO.setup(LED,GPIO.OUT)  #initialize GPIO21 (LED) as an output Pin
GPIO.output(LED,0)


server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )

port = 1
server_socket.bind(("",port))
server_socket.listen(1)

client_socket,address = server_socket.accept()
threads = []

print "Accepted connection from ",address
while 1:

	data = client_socket.recv(1024)
	print "Received: %s" % data
 	if (data == "0"):    #if '0' is sent from the Android App, turn OFF the LED
 		print ("GPIO 21 LOW, LED OFF")
 		GPIO.output(LED,0)
 	if (data == "1"):    #if '1' is sent from the Android App, turn OFF the LED
 		print ("GPIO 21 HIGH, LED ON")
 		GPIO.output(LED,1)
 		t = threading.Thread(target=vidworker)
 		threads.append(t)
 		t.start()
 	if (data == "2"):
 		print ("Recording Data!")	
 		t2 = threading.Thread(target=altworker)
 		threads.append(t2)
 		t2.start()
 	if (data == "q"):
 		print ("Quit")
 		break

def altworker():
    """thread worker function"""
    f = open("bt-activated-data-recording.txt","w") 

	for i in range(0, 300):
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
    return 

def vidworker():
	"""thread worker function"""
	camera = picamera.PiCamera()
 	camera.resolution = (1280, 720)
 	camera.start_recording('bt-activated-video.h264')
 	camera.wait_recording(300)
 	camera.stop_recording()
 	return

