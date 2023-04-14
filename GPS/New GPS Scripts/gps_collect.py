import time
import serial
from datetime import datetime, timezone

import csv

#Good resource on NMEA-0183 Sentence structure and associated data
# https://w3.cs.jmu.edu/bernstdh/web/common/help/nmea-sentences.php

#GPGGA data = Global Positioning system fix data. This contains the values we want to record

#Fix states are as follows:
# 1 = Valid
# 2 = Valid (SBAS)
# 3 = Invalid

header = ["SysTime [UTC]", "GPS Time [UTC]", "Lat [DD]", "Lon [DD]", "Alt [m]", "SatCount [-]", "Fix [-]"] 

data_out_file_name = "/home/albertasat/DEBORA/Sensors/Data/GPS_data/test_data.csv"

def write_to_csv_file(data_line):
    # open the file
    f = open(data_out_file_name, 'a')
    # init the writer
    writer = csv.writer(f)
    # write the data 
    writer.writerow(data_line)
    # close the file 
    f.close()
    return 

#Initialize serial object
def init_serial_obj():
	serial_obj = serial.Serial(
        port = '/dev/ttyS0',
        baudrate = 4800,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 1
        )
	return serial_obj

# Function to parse NMEA DDM to DD
def nmea_parse(gpgga):
	# Get DD format
	deg = round(float(gpgga[:-8]), 6)
	minute = round(float(gpgga[-8:]) / 60, 6)
	return str(deg + minute)

def config_gps(serial_obj):
	# Sends command to put in air mode, and high sensitivity
	time.sleep(0.7)
	txAir = "$PTNLSCR,,,,,,,3,,*5B\r\n"
	txHiSense = "$PTNLSFS,H,0*38\r\n"
	serial_obj.write(txAir.encode())
	serial_obj.write(txHiSense.encode())
	return

def query_gps(serial_obj):
	NMEA_sentence = serial_obj.readline().decode()
		
	# Checks for valid NMEA 0183 sentence:
	if NMEA_sentence[0] == "$":
		# Splitting NMEA Sentence
		NMEA_sentence_arr = NMEA_sentence.split(",")

        # If our sentence is not of type GGA, we will ignore it
		if NMEA_sentence_arr[0] == "$GPGGA":
			# Gets GPS UTC time (of fix) from NMEA sentence (from GPS satellite)
			if len(NMEA_sentence_arr[1]) == 6+3:
				split_time = (NMEA_sentence_arr[1]).split(".")
				split_time = split_time[0]
				gps_time = split_time[:2] + ":" + split_time[2:4]+ ":" + split_time[-2:]
			else:
				gps_time = " - " # If unable to retrieve UTC time from GPS Satallite

			#Get GPS fix
            fix_state = NMEA_sentence_arr[6]

            #Get satellite count
			sat = NMEA_sentence_arr[7].lstrip("0")

			# Extracting DDM latitude, longitude and altitude
			if len(NMEA_sentence_arr[2]) > 0:
				lat = nmea_parse(NMEA_sentence_arr[2])
				lon = nmea_parse(NMEA_sentence_arr[4])
            else:
                lat = " - "
                lon = " - "
				
            #Get altitude above mean sea level
			if len(NMEA_sentence_arr[9]) != 0:
                alt = NMEA_sentence_arr[9].lstrip("0")
            else:
                alt = " - "

            # Create array from GPS data 
            gps_data = []
            gps_data.append(gps_time)
            gps_data.append(lat)
            gps_data.append(lon)
            gps_data.append(alt)
            gps_data.append(sat)
            gps_data.append(fix_state)
            
            return gps_data

	return -1


if __name__ == '__main__':
    #write the header row 
    write_to_file(header)
    
    #initialize the serial port 
    serial_obj = init_serial_obj()

	#configure the gps
	config_gps(serial_obj)

    print("\nBeginning data collection... \n")
    #Begin inf loop writing data to file.
    while True:
        # fetch gps data. 
        #If -1 returned, data was not fetched and ignore this loop
		gps_data = query_gps(serial_obj)

        if gps_data == -1:
            continue
        else:    
            #fetch system time
            sys_time = datetime.utcnow().strftime("%Y%m%dT%H:%M:%S.%f")

            #create string array containing sys time and icm data
            data_row = [sys_time]
			data_row.extend(gps_data)

            #write data row to csv file
            write_to_file(data_row)

        time.sleep(0.1)