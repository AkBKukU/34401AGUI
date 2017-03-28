#!/usr/bin/python

import time
import serial

def reset():
	ser.write("*RST\n") # Reset
	ser.write("*CLS\n") # Reset
	ser.write("SYST:REM\n") # Set to remote mode
	ser.write("CONF:VOLT:DC 15, 0.1\n") # Set high max and low resolution DC voltage mesurement
	ser.write("SAMP:COUN 5\n") # Set high max and low resolution DC voltage mesurement
	time.sleep(1)

def errorCheck():
	ser.write("SYST:ERR?\n")
	time.sleep(0.5)
	line = ser.readline().replace("\n","")
	while (line.find("+0") == -1):
		print(line)
		ser.write("SYST:ERR?\n")
		time.sleep(0.5)
		line = ser.readline().replace("\n","")

ser = serial.Serial('/dev/ttyUSB0')
ser.baudrate = 9600
ser.bytesize = 7
ser.parity = 'E'
ser.stopbits = 2

reset()
print(ser.name)

ser.write("READ?\n") # Reset
line = ser.readline()

print(str(float(line)))


errorCheck()

ser.close()