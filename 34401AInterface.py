#!/usr/bin/python

import sys
import time
import serial
import glob
from PySide import QtCore, QtGui
from ui_mainWindow import Ui_MainWindow
from ui_helpWindow import Ui_Dialog
from DMM import DMM34401A

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

		# Logging
		self.ui.logResHelp.clicked.connect(self.showHelp)
		self.ui.logStart.clicked.connect(self.configureRepeat)

	def showHelp(self):
		self.reshelp.show()

	# Load file from server
	def connect(self):
		self.dmm = DMM34401A(self.ui.serialDevice.currentText())
		eggdelay = 0.15
		self.dmm.setdisplayText(" -- EGGMETER")
		time.sleep(eggdelay)
		self.dmm.setdisplayText("-- EGGMETER ")
		time.sleep(eggdelay)
		self.dmm.setdisplayText("- EGGMETER 5")
		time.sleep(eggdelay)
		self.dmm.setdisplayText(" EGGMETER 50")
		time.sleep(eggdelay)
		self.dmm.setdisplayText("EGGMETER 500")
		time.sleep(eggdelay)
		self.dmm.setdisplayText("GGMETER 5000")
		time.sleep(eggdelay)
		self.dmm.setdisplayText("GMETER 5000 ")
		time.sleep(eggdelay)
		self.dmm.setdisplayText("METER 5000 -")
		time.sleep(eggdelay)
		self.dmm.setdisplayText("ETER 5000 --")
		time.sleep(eggdelay)
		self.dmm.setdisplayText("TER 5000 -- ")

		self.dmm.setdisplayClear()

	# Load file from server
	def reset(self):
		self.dmm.reset()
		eggdelay = 0.15
		self.dmm.setdisplayText(" -- EGGMETER")
		time.sleep(eggdelay)
		self.dmm.setdisplayText("-- EGGMETER ")
		time.sleep(eggdelay)
		self.dmm.setdisplayText("- EGGMETER 5")
		time.sleep(eggdelay)
		self.dmm.setdisplayText(" EGGMETER 50")
		time.sleep(eggdelay)
		self.dmm.setdisplayText("EGGMETER 500")
		time.sleep(eggdelay)
		self.dmm.setdisplayText("GGMETER 5000")
		time.sleep(eggdelay)
		self.dmm.setdisplayText("GMETER 5000 ")
		time.sleep(eggdelay)
		self.dmm.setdisplayText("METER 5000 -")
		time.sleep(eggdelay)
		self.dmm.setdisplayText("ETER 5000 --")
		time.sleep(eggdelay)
		self.dmm.setdisplayText("TER 5000 -- ")

		self.dmm.setdisplayClear()

	# Load file from server
	def beeperControl(self):
		self.dmm.setBeeper(self.ui.beepEnable.checkState())

	# Load file from server
	def displayControl(self):
		self.dmm.setdisplay(self.ui.displayEnable.checkState())

	def quickMeasurement(self):
		self.dmm.setMeasurementMode(self.ui.quickMeasureMode.currentIndex())
		self.dmm.setResolution(self.ui.quickResOverload.text(),self.ui.quickResLowerLimit.text())
		reading = self.dmm.takeMeasurement()
		self.ui.lastMeasurement.setText(str(reading))
		self.ui.lastMeasureMode.setText(self.dmm.getModeName())

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

	def configureRepeat(self):
		if( self.isLogging == 0) : 

			if( self.configured == 0) :
				print "Configure Logging"

				self.dmm.setMeasurementMode(self.ui.logMeasureMode.currentIndex())
				self.dmm.setResolution(self.ui.logResOverload.text(),self.ui.logResLowerLimit.text())

				self.configured = 1
				self.isLogging = 1
				self.stopLogging = 0
			
			if( self.ui.logTrigSource.currentIndex() == 0) :

				self.logtimer = QtCore.QTimer(self)
				self.logtimer.timeout.connect(self.repeatAction)
				self.logtimer.start((self.ui.logAutoInterval.value() * 1000))
				self.ui.logStart.setText("Stop Logging")
				

			if( self.ui.logTrigSource.currentIndex() == 1) :

				self.isLogging = 1
				self.configured = 1
				carryOutLog = 1
				self.repeatAction()
				self.ui.logStart.setText("Take Measurement")

		else:


			if( self.ui.logTrigSource.currentIndex() == 1) :

				self.isLogging = 1
				self.configured = 1
				carryOutLog = 1
				self.repeatAction()
				self.ui.logStart.setText("Take Measurement")
			else:
				self.ui.logStart.setText("Start Logging")
				self.stopLogging = 1
				self.isLogging = 0
				self.configured = 0


	def repeatAction(self):
		print "Log Action"

		if( self.stopLogging ):

			self.logtimer.stop()

		reading = self.dmm.takeMeasurement()
		self.ui.lastMeasurement.setText(str(reading))
		self.ui.lastMeasureMode.setText(self.dmm.getModeName())


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
