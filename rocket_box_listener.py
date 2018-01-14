from bluetooth import *
import RPi.GPIO as GPIO        #calling for header file which helps in using GPIOs of PI
import time
import logging
 
bd_addr = "98:D3:31:50:3A:86" #Rocketbox Address
port = 1

while 1:
	socket=BluetoothSocket( RFCOMM )
	socket.connect((bd_addr, port))
	socket.send("RSV Connected")
	time.sleep(2)

	try:
		while 1:
			socket.send("Sending Data")
			time.sleep(3)
	finally:
		socket.close()	