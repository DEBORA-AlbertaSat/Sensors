##########################################################################################
#
# This python script is used to Read and parse GPS data from the GPS Module Copernicus II 
# It saves two files. The first file saves the raw NMEA 0183 sentences, while the 
# other file saves the DD latitude and longitude parsed from the NMEA 0183 sentences
#
##########################################################################################
#
# Written by Ryan Bererton and Destin Chan
#
##########################################################################################

import time
import serial
import datetime

Date = str(datetime.date.today())
nmeaFile = "NMEA_Data_" + Date + ".txt"
gpsFile = "GPS_Data_" + Date + ".txt"

ser = serial.Serial(
        port = '/dev/ttyS0',
        baudrate = 4800,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 1
        )

# Function to parse NMEA DDM to DD
def nmeaParse(gpgga):
	# Get DD format
	deg = round(float(gpgga[:-8]), 6)
	minute = round(float(gpgga[-8:]) / 60, 6)
	return str(deg + minute)

# Sends command to put in air mode, and high sensitivity
time.sleep(0.7)
txAir = "$PTNLSCR,,,,,,,3,,*5B\r\n"
txHiSense = "$PTNLSFS,H,0*38\r\n"
ser.write(txAir.encode())
ser.write(txHiSense.encode())

while 1:
	opData = ser.readline().decode()
	locTimestamp = "[" + time.strftime("%H:%M:%S,", time.localtime()) # Get's local time
	print(locTimestamp + opData)
		
	# Checks for valid NMEA 0183 sentence:
	if opData[0] == "$":
		# Writes Raw NMEA transmissions to a file
		with open(nmeaFile, 'a', encoding = 'utf-8') as NMEA_File:    
			NMEA_File.writelines(locTimestamp + opData)

		# Splitting NMEA Sentence
		validGPS = opData.split(",")
		if validGPS[0] == "$GPGGA":
			# Gets GPS UTC time (of fix) from NMEA sentence (from satellite)
			if len(validGPS[1]) == 6+3:
				splitTime = (validGPS[1]).split(".")
				splitTime = splitTime[0]
				utcTime = "(UTC " + splitTime[:2] + ":" + splitTime[2:4]+ ":" + splitTime[-2:] + ")] "
			else:
				utcTime = "(UTC --:--:--)] " # If unable to retrieve UTC time from GPS Satallite

			# Combines Local (RPi) + UTC Timestamp (GPS Satellite)
			timestamps = locTimestamp + utcTime
			
			# Check if valid GPS fix + # of satellites
			fixQuality = validGPS[6]
			if fixQuality == "1":
				fixState = "GPS Fix: Valid"
			elif fixQuality == "2":
				fixState = "GPS Fix: Valid (SBAS)"
			else:
				fixState = "GPS Fix: Invalid"

			sat = "# of Sats: " + validGPS[7].lstrip("0") + ", "

			# Extracting DDM latitude, longitude and altitude
			if len(validGPS[2]) > 0:
				lat = nmeaParse(validGPS[2])
				lon = nmeaParse(validGPS[4])
				
				loc = "Lat/Lon: (" + lat + "," + lon + "), "

				if len(validGPS[9]) != 0:
					alt = "Alt: " + validGPS[9].lstrip("0") + " m, "
				else:
					alt = "Alt: XXX m, "

				# Writes Parsed GPS data to a separate file
				with open(gpsFile, 'a', encoding = 'utf-8') as GPS_File:    
					GPS_File.writelines(timestamps + loc + alt + sat + fixState + "\n")

			else: # len(validGPS[2]) == 0:
				with open(gpsFile, 'a', encoding = 'utf-8') as GPS_File:
					GPS_File.writelines(timestamps + "Lat/Lon: (XXX,XXX), Alt: XXX m, " + sat + fixState + "\n")
