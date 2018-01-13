from bluetooth import *
import RPi.GPIO as GPIO        #calling for header file which helps in using GPIOs of PI
import time
import logging

socket=BluetoothSocket( RFCOMM )
 
bd_addr = "98:D3:31:50:3A:86" #Rocketbox Address
port = 1

socket.connect((bd_addr, port))
socket.send("RSV BT Connection Established")

try:
	while 1:
		#data = socket.recv(1024)
		socket.send("Sending Data")
		time.sleep(1)

except KeyboardInterrupt:  
		# here you put any code you want to run before the program   
		# exits when you press CTRL+C  
	#camera.close()
	#f.close()

finally:  
	GPIO.cleanup() # this ensures a clean exit     