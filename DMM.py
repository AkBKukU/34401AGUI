#!/usr/bin/python

import sys
import time
import serial

class DMM34401A:
		
	# Constructor
	# Initialize connection to DMM
	def __init__(self,connectionPath, baud, par):
		# Configure serial connection
		self.ser = serial.Serial(connectionPath)
		self.ser.baudrate = int(baud)
		self.ser.bytesize = 8
		self.ser.parity = par[:1]
		self.ser.stopbits = 2
		self.ser.xon_xoff = True

		# DMM Commands
		self.sep = ":"
		self.delim = ", "
		self.CONF = "CONF"
		self.SAMP = "SAMP"
		self.TRIG = "TRIG"
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
		self.COUN = ":COUN "
		self.DEL = ":DEL "
		self.DIOD = ":DIOD "
		self.DC = "DC "
		self.AC = "AC "
		self.VOLTDC = self.VOLT+self.DC
		self.VOLTAC = self.VOLT+self.AC
		self.CURRDC = self.CURR+self.DC
		self.CURRAC = self.CURR+self.AC

		# Default values
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

	# Clear all registers on DMM
	def reset(self):
		self.serWrite(self.RST) # Reset
		self.serWrite(self.CLS) # Reset
		self.serWrite(self.SYST+self.REM) # Set to remote mode
		time.sleep(1)

	# Return the current measureing mode ID
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

	# Return the current measureing mode name
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

	# Set the current measureing mode
	def setMeasurementMode(self,measurementMode):

		self.measurementMode = self.getMode(measurementMode)
		self.writeConf()

	# Set the current resolution
	def setResolution(self,overload,lowerLimit):
		self.overload = overload
		self.lowerLimit = lowerLimit
		self.writeConf()

	# Get a reading from the DMM
	def takeMeasurement(self):
		self.serWrite(self.READ) 
		output = self.ser.readline()
		result = output.split(',')
		return result

	# Send CONF command for setting mode an resolution
	def writeConf(self):
		# Set high max and low resolution mesurement mode
		if( self.measurementMode == self.CONT ) or ( self.measurementMode == self.DIOD ):
			parameters = ""
		else:
			parameters = str(self.overload) + self.delim + str(self.lowerLimit)

		self.serWrite(self.CONF+self.measurementMode+parameters) 
		time.sleep(1) # Wait for it to take

	# Send a command to the DMM
	def serWrite(self,data):
		print "Sending: " + data
		self.ser.write(data+"\n")

	# Get error messages from DMM
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

	# Set the number of samples to take per trigger
	def setSampleCount(self,samples):
		self.serWrite(self.SAMP + self.COUN+str(samples))

	# Set delay between multiple samples per trigger
	def setTriggerDelay(self,delay):
		self.serWrite(self.TRIG + self.DEL+str(delay))

	# Turn display on or off
	def setdisplay(self,state):
		self.display = state
		if( self.display ):
			self.serWrite(self.DISP + " " + self.ON)
		else:
			self.serWrite(self.DISP + " " + self.OFF)

	# Write text to display
	def setdisplayText(self,text):
		self.serWrite(self.DISP + self.TEXT + " \"" + text + "\"")

	# Reset display to normal
	def setdisplayClear(self):
		self.serWrite(self.DISP + self.TEXT + self.CLE)

	# Turn beeper on or off
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
