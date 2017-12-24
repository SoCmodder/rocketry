from bluetooth import *
import RPi.GPIO as GPIO        #calling for header file which helps in using GPIOs of PI
import picamera
import datetime
import time
import threading
import BMP280 as BMP280
import logging

sensor = BMP280.BMP280()

GPIO.setmode(GPIO.BCM)     #programming the GPIO by BCM pin numbers. (like PIN40 as GPIO21)
GPIO.setwarnings(False)
GPIO.setup(LED,GPIO.OUT)  #initialize GPIO21 (LED) as an output Pin
GPIO.output(LED,0)

camera = picamera.PiCamera()
camera.resolution = (1280, 720)

server_socket=BluetoothSocket( RFCOMM )
 
port = 1
server_socket.bind(("",port))
server_socket.listen(1)

uuid = "fa87c0d0-afac-11de-8a39-0800200c9a66"

advertise_service( server_socket, "RSV",
                   service_id = uuid,
                   service_classes = [ uuid, SERIAL_PORT_CLASS ],
                   profiles = [ SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )

threads = []

def altworker():
  """thread worker function"""
  f = open("bt-activated-data-recording.txt","w") 
  for i in range(0, 960):
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
  client_socket.send("Finished Altitude Data Recording!\n")
  return 

def vidworker():
  """thread worker function"""
  camera.start_recording('bt-activated-video.h264')
  camera.wait_recording(960)
  camera.stop_recording()
  client_socket.send("Finished Recording Video")
  return

initAlt = sensor.read_altitude()  
 
client_socket,address = server_socket.accept()
print "Accepted connection from ",address
while 1:
 
  data = client_socket.recv(1024)
  print "Received: %s" % data

  if (data == "1"):    #if '0' is sent from the Android App, turn OFF the LED
    client_socket.send("Recording Video!\n")
    t = threading.Thread(target=vidworker)
    threads.append(t)
    t.start()
  if (data == "2"):    #if '1' is sent from the Android App, turn OFF the LED
    client_socket.send("Recording Data!\n")
    t2 = threading.Thread(target=altworker)
    threads.append(t2)
    t2.start()
  if (data == "q"):
    print ("Quit")
    client_socket.send("Quit command accepted: Shutting Down All Recording!")
    break
  client_socket.send('Altitude = {0:0.2f} m'.format(sensor.read_altitude() - initAlt) + '\n')

camera.close()
f.close()

client_socket.close()
server_socket.close()