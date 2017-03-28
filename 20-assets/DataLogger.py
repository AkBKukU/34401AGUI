#!/usr/bin/python

import sys
import time

class DataLogger:
		
	# Constructor
	# Initialize connection to DMM
	def __init__(self):
		self.filePath = ""
		self.fileStatus = 0
		self.file = None

	# "Destructor"-ish
	# Close connection to server
	def __del__(self):


# Check if script run directly
if __name__ == '__main__':

	# Initialize MainWindow 
	log = DataLogger()

	# Execute window loop and exit on completion
	sys.exit()