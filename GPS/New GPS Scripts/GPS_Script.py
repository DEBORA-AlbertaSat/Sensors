# This python script is used to Read GPS data from the GPS Module Copernicus II
#

import time
import serial
import datetime

Date = str(datetime.date.today())
nemaFile = "NEMA_Data_" + Date + ".txt"
gpsFile = "GPS_Data_" + Date + ".txt"

ser = serial.Serial(
        port = '/dev/ttyS0',
        baudrate = 4800,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 1
        )

while 1:
	Data = ser.readline().decode()
	locTimestamp = time.strftime("%H:%M:%S,UTC%z", time.localtime()) # Get's local time + UTC offset
	nemaData = "[" + locTimestamp + "] " + Data
	print(nemaData)
	
	# Writes Raw NEMA transmissions to a file
	with open(nemaFile, 'a', encoding = 'utf-8') as NEMA_File:    
		NEMA_File.writelines(nemaData)
	
	# Writes Parsed GPS data to a separate file
	# with open(gpsFile, 'a', encoding = 'utf-8') as GPS_File:    
		# GPS_File.writelines(gpsData)	
