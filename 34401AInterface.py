#!/usr/bin/python2

import sys
import time
import serial
import glob
from PySide import QtCore, QtGui
from ui_mainWindow import Ui_MainWindow
from ui_helpWindow import Ui_Dialog
from DMM import DMM34401A
import datetime
import numpy as np

# Import class created by pyside-uic from the ui file
class MainWindow(QtGui.QMainWindow):
	
	# Constructor
	# Initializes ui
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)

		# Get ui object
		self.ui = Ui_MainWindow()

		# Initialize ui
		self.ui.setupUi(self)
		self.isLogging = 0
		self.configured = 0
		self.sampleLimit = 0

		# Initialize event handlers
		self.assignWidgets()
		self.getSerialPorts()
	
	# Event handler assignments 
	def assignWidgets(self):
		
		# Quick Measurement
		self.ui.quickResHelp.clicked.connect(self.showHelp)
		self.ui.quickTakeMeasurement.clicked.connect(self.quickMeasurement)

		# Settings
		self.ui.connectToDevice.clicked.connect(self.connect)
		self.ui.beepEnable.stateChanged.connect(self.beeperControl)
		self.ui.displayEnable.stateChanged.connect(self.displayControl)
		self.ui.systReset.clicked.connect(self.reset)
		self.ui.viewErrors.clicked.connect(self.showErrors)

		# Logging
		self.ui.logFileBrowse.clicked.connect(self.getLogFilePath)
		self.ui.logResHelp.clicked.connect(self.showHelp)
		self.ui.logStart.clicked.connect(self.configureRepeat)
		self.ui.loggingStop.clicked.connect(self.loggingStop)
		self.ui.dataNotes.returnPressed.connect(self.configureRepeat)


	def showHelp(self):
		self.reshelp.show()

	# Load file from server serialBaudRate
	def connect(self):
		self.dmm = DMM34401A(self.ui.serialDevice.currentText(),self.ui.serialBaudRate.currentText(),self.ui.serialParity.currentText() )
		self.reset()

	# Load file from server
	def reset(self):
		self.dmm.reset()
		delay = 1
		self.dmm.setdisplayText("AkBKukU")
		time.sleep(delay)
		self.dmm.setdisplayClear()
		self.dmm.setSampleCount(1)
		self.dmm.setTriggerDelay(0)

	def showErrors(self):
		QtGui.QMessageBox.information(
			self,
			'Stored Errors',
			self.dmm.errorCheck(),
			0
			)

	# Load file from server
	def beeperControl(self):
		self.dmm.setBeeper(self.ui.beepEnable.checkState())

	# Load file from server
	def displayControl(self):
		self.dmm.setdisplay(self.ui.displayEnable.checkState())

	# Open a dialog to get a filepath for the log
	def getLogFilePath(self):
		fileName , other= QtGui.QFileDialog.getSaveFileName(self, 'Save log as', '', selectedFilter='*.csv')

		# Add ".csv" to the end of the filename if not present
		if( not fileName.endswith(".csv") ):
			fileName = str(fileName)+".csv"

		print fileName
		
		# Set the text input to the file path
		self.ui.logFilePath.setText(str(fileName))


	# Get measurement from DMM and put it in last measurement
	def quickMeasurement(self):
		self.dmm.setMeasurementMode(self.ui.quickMeasureMode.currentIndex())
		self.dmm.setResolution(self.ui.quickResOverload.text(),self.ui.quickResLowerLimit.text())
		reading = self.dmm.takeMeasurement()
		print str(reading)
		reading = float(reading[0])
		self.setLastMesurement(reading,self.dmm.getModeName())

	# Set the last measured feilds
	def setLastMesurement(self,value,mode):
		self.ui.lastMeasurement.setText(str(value))
		self.ui.lastMeasureMode.setText(str(mode))

	# Get a list of all availible serial port to give the user
	def getSerialPorts(self):
		if sys.platform.startswith('win'):
			ports = ['COM%s' % (i + 1) for i in range(256)]
		elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
			# this excludes your current terminal "/dev/tty"
			ports = glob.glob('/dev/tty[A-Za-z]*')
		elif sys.platform.startswith('darwin'):
			ports = glob.glob('/dev/tty.*')
		else:
			raise EnvironmentError('Unsupported platform')

		result = []
		for port in ports:
			try:
				s = serial.Serial(port)
				s.close()
				result.append(port)
			except (OSError, serial.SerialException):
				pass

		for device in result:
			self.ui.serialDevice.addItem(device)

	# Logging start button logic
	def configureRepeat(self):
		if( self.isLogging == 0) : 

			# Inital configureation for log session
			if( self.configured == 0) :
				print "Configure Logging"

				# Update DMM with current settings
				self.dmm.setMeasurementMode(self.ui.logMeasureMode.currentIndex())
				self.dmm.setResolution(self.ui.logResOverload.text(),self.ui.logResLowerLimit.text())

				self.dmm.setSampleCount(self.ui.logTriggerSampleCount.value())
				self.dmm.setTriggerDelay(self.ui.logTriggerSampleDelay.value())

				# Set logic variables
				self.configured = 1
				self.isLogging = 1
				self.stopLogging = 0

				# Clear file if set to replace
				if( not self.ui.logFilePath.text() == "" ):
					print "Opening the file..."

					if(self.ui.logReplace.isChecked()):
						logFile = open(self.ui.logFilePath.text(), 'w')
						logFile.truncate()
						logFile.close()

			# Automatic mode configure
			if( self.ui.logTrigSource.currentIndex() == 0) :

				# Start timer to call function
				self.logtimer = QtCore.QTimer(self)
				self.logtimer.timeout.connect(self.repeatAction)
				self.logtimer.start((self.ui.logAutoInterval.value() * 1000))

				# Set the limit of samples to take
				self.sampleLimit = self.ui.logAutoSamplesMax.value()
				self.ui.logStart.setText("Stop Logging")

				

			# Manual mode configure
			if( self.ui.logTrigSource.currentIndex() == 1) :

				self.isLogging = 1
				self.configured = 1
				carryOutLog = 1
				self.ui.logStart.setText("Take Measurement")

		else:

			# Manual mode Take sample
			if( self.ui.logTrigSource.currentIndex() == 1) :

				self.isLogging = 1
				self.configured = 1
				carryOutLog = 1
				self.repeatAction()
				self.ui.logStart.setText("Take Measurement")

			# Default
			else:
				self.ui.logStart.setText("Start Logging")
				self.stopLogging = 1
				self.isLogging = 0
				self.configured = 0

	# End loggin session
	def loggingStop(self):
		self.stopLogging = 1
		self.ui.logStart.setText("Start Logging")
		self.isLogging = 0
		self.configured = 0


	# Log function to collect and store data
	def repeatAction(self):
		print "Log Action"

		# Keep filepath from changing
		self.ui.logFilePath.setReadOnly(True)

		# Check if loggin over
		if( self.stopLogging ):

			self.logtimer.stop()
			self.ui.logFilePath.setReadOnly(False)
		else:

			# Get measurement from DMM
			reading = self.dmm.takeMeasurement()
			# Convert from list of strings to list of floats
			reading = np.array(map(float, reading))
			# Set last measurement
			self.setLastMesurement(reading[0],self.dmm.getModeName())
			
			# Check if samples are limited and subtract 1
			if( not self.ui.logAutoSamplesLimit.isChecked() ):
				self.sampleLimit -= 1

				# Stop measuring when limit reached
				if( not self.sampleLimit ):
					self.loggingStop()

			# Check if file is set
			if( not self.ui.logFilePath.text() == "" ):
				# Log data to file
				parsed = str(reading).replace("[ ","").replace("[","").replace("]","").replace("  ",",").replace(" ",",")
				logFile = open(self.ui.logFilePath.text(), 'a')
				now = '%s' % datetime.datetime.now()
				date, time = now.split(" ")
				notes = self.ui.dataNotes.text()
				logFile.write(str(date)+","+str(time)+","+str(notes)+","+parsed+"\n")
				logFile.close()


# Import class created by pyside-uic from the ui file
class Dialog(QtGui.QDialog):
	# Constructor
	# Initializes ui
	def __init__(self, parent=None):
		super(Dialog, self).__init__(parent)

		# Get ui object
		self.helpui = Ui_Dialog()

		# Initialize ui
		self.helpui.setupUi(self)


# Check if script run directly
if __name__ == '__main__':
	# Initialize QT 
	app = QtGui.QApplication(sys.argv)

	# Initialize MainWindow 
	window = MainWindow()
	# Initialize MainWindow 
	window.reshelp = Dialog()

	# Display window
	window.show()

	# Execute window loop and exit on completion
	sys.exit(app.exec_())
