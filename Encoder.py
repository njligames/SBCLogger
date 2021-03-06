
from DeviceInfo import DisplayAttachedDeviceInfo
from DeviceInfo import DisplayDetachedDeviceInfo
from DeviceInfo import DisplayErrorDeviceInfo

from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException

from Phidgets.Events.Events import EncoderPositionChangeEventArgs, PositionChangeEventArgs, InputChangeEventArgs, AttachEventArgs, DetachEventArgs, ErrorEventArgs
from Phidgets.Devices.Encoder import Encoder

import datetime
import sqlite3

def AttachEncoder(databasepath, serialNumber):
	def onAttachHandler(event):
		logString = "Encoder Attached " + str(event.device.getSerialNum())
		#print(logString)
		DisplayAttachedDeviceInfo(event.device)

	def onDetachHandler(event):
		logString = "Encoder Detached " + str(event.device.getSerialNum())
		#print(logString)
		DisplayDetachedDeviceInfo(event.device)

		event.device.closePhidget()

	def onErrorHandler(event):
		logString = "Encoder Error " + str(event.device.getSerialNum()) + ", Error: " + event.description
		print(logString)

		DisplayErrorDeviceInfo(event.device)
		
	def onServerConnectHandler(event):
		logString = "Encoder Server Connect " + str(event.device.getSerialNum())
		#print(logString)

	def onServerDisconnectHandler(event):
		logString = "Encoder Server Disconnect " + str(event.device.getSerialNum())
		#print(logString)

	def inputChangeHandler(event):
		logString = "Encoder Input Changed"
		#print(logString)

		try:
			conn = sqlite3.connect(databasepath)
				
			conn.execute("INSERT INTO ENCODER_INPUTCHANGE VALUES(NULL, DateTime('now'), ?, ?, ?)",
					(event.device.getSerialNum(), event.index, int(event.state)))

			conn.commit()
			conn.close()
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]

	def positionChangeHandler(event):
		logString = "Encoder Position Changed"
		#print(logString)

		try:
			conn = sqlite3.connect(databasepath)

			conn.execute("INSERT INTO ENCODER_POSITIONCHANGE VALUES(NULL, DateTime('now'), ?, ?, ?)",
					(event.device.getSerialNum(), event.index, event.position))

			conn.commit()
			conn.close()
		except sqlite3.Error as e:
			print "An error occurred:", e.args[0]

	try:
		p = Encoder()

		p.setOnAttachHandler(onAttachHandler)
		p.setOnDetachHandler(onDetachHandler)
		p.setOnErrorhandler(onErrorHandler)
		p.setOnServerConnectHandler(onServerConnectHandler)
		p.setOnServerDisconnectHandler(onServerDisconnectHandler)

		p.setOnInputChangeHandler(inputChangeHandler)
		p.setOnPositionChangeHandler(positionChangeHandler)

		p.openPhidget(serialNumber)

	except PhidgetException as e:
		print("Phidget Exception %i: %s" % (e.code, e.details))
		print("Exiting...")
		exit(1)

