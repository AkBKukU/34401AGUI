#!/usr/bin/python

import sys
import time
import serial

class DMM34401A:
		
	# Constructor
	# Initialize connection to DMM
	def __init__(self,connectionPath):
		self.ser = serial.Serial(connectionPath)
		self.ser.baudrate = 9600
		self.ser.bytesize = 7
		self.ser.parity = 'E'
		self.ser.stopbits = 2


		self.sep = ":"
		self.delim = ", "
		self.CONF = "CONF"
		self.RST = "*RST"
		self.CLS = "*CLS"
		self.SYST = "SYST"
		self.BEEP = ":BEEP"
		self.STAT = ":STAT "
		self.DISP = "DISP"
		self.TEXT = ":TEXT"
		self.CLE = ":CLE "
		self.ON = "ON"
		self.OFF = "OFF"
		self.ERR = ":ERR?"
		self.REM = ":REM"
		self.VOLT = ":VOLT:"
		self.CURR = ":CURR:"
		self.RES = ":RES "
		self.FRES = ":FRES "
		self.FRE = ":FREQ "
		self.PER = ":PER "
		self.CONT = ":CONT "
		self.DIOD = ":DIOD "
		self.DC = "DC "
		self.AC = "AC "
		self.VOLTDC = self.VOLT+self.DC
		self.VOLTAC = self.VOLT+self.AC
		self.CURRDC = self.CURR+self.DC
		self.CURRAC = self.CURR+self.AC

		self.overload = 10
		self.lowerLimit = 0.01
		self.measurementMode = self.DC

		self.READ = "READ?"

		self.beeper = 1
		self.display = 1

		self.reset()


	# "Destructor"-ish
	# Close connection to server
	def __del__(self):
		self.ser.close()

	def reset(self):
		self.serWrite(self.RST) # Reset
		self.serWrite(self.CLS) # Reset
		self.serWrite(self.SYST+self.REM) # Set to remote mode
		time.sleep(1)


	def getMode(self,i):
		return {
			0 : self.VOLTDC,
			1 : self.CURRDC,
			2 : self.VOLTAC,
			3 : self.CURRAC,
			4 : self.RES,
			5 : self.FRES,
			6 : self.FRE,
			7 : self.PER,
			8 : self.CONT,
			9 : self.DIOD
		}[i]

	def getModeName(self,i=""):

		if (i == ""):
			i = self.measurementMode

		return {
			self.VOLTDC : "DC Voltage",
			self.CURRDC : "DC Current",
			self.VOLTAC : "AC Voltage",
			self.CURRAC : "AC Current",
			self.RES : "Resistance",
			self.FRES : "4 Wire Resistance",
			self.FRE : "Frequency",
			self.PER : "Period",
			self.CONT : "Continuity",
			self.DIOD : "Diode"
		}[i]

	def setMeasurementMode(self,measurementMode):

		self.measurementMode = self.getMode(measurementMode)
		self.writeConf()

	def setResolution(self,overload,lowerLimit):
		self.overload = overload
		self.lowerLimit = lowerLimit
		self.writeConf()

	def takeMeasurement(self):
		self.serWrite(self.READ) 
		return float(self.ser.readline())

	def writeConf(self):
		# Set high max and low resolution DC voltage mesurement
		if( self.measurementMode == self.CONT ) or ( self.measurementMode == self.DIOD ):
			parameters = ""
		else:
			parameters = str(self.overload) + self.delim + str(self.lowerLimit)

		self.serWrite(self.CONF+self.measurementMode+parameters) 
		time.sleep(1)

	def serWrite(self,data):
		print "Sending: " + data
		self.ser.write(data+"\n")


	def errorCheck(self):
		self.serWrite(self.SYST+self.ERR)
		time.sleep(0.5)
		errors = ""
		line = self.ser.readline().replace("\n","")
		while (line.find("+0") == -1):
			print(line)
			errors += line+"\n"
			self.serWrite(self.SYST+self.ERR)
			time.sleep(0.5)
			line = self.ser.readline().replace("\n","")

		return errors


	def setdisplay(self,state):
		self.display = state
		if( self.display ):
			self.serWrite(self.DISP + " " + self.ON)
		else:
			self.serWrite(self.DISP + " " + self.OFF)

	def setdisplayText(self,text):
		self.serWrite(self.DISP + self.TEXT + " \"" + text + "\"")

	def setdisplayClear(self):
		self.serWrite(self.DISP + self.TEXT + self.CLE)

	def setBeeper(self,state):
		self.beeper = state
		if( self.beeper ):
			self.serWrite(self.SYST + self.BEEP+self.STAT+self.ON)
		else:
			self.serWrite(self.SYST + self.BEEP+self.STAT+self.OFF)

# Check if script run directly
if __name__ == '__main__':

	# Initialize MainWindow 
	dmm = DMM34401A('/dev/ttyUSB0')
	dmm.setResolution(22,0.9)
	dmm.errorCheck()


	print dmm.takeMeasurement()
	# Execute window loop and exit on completion
	sys.exit()