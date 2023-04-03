
from __future__ import print_function
import qwiic_bme280
import time
import sys

import csv

from datetime import datetime, timezone

header = ["SysTime, Humidity, Pressure, Altitude, Temperature"]

data_out_file_name = "~/DEBORA/Sensors/Data/bme280_data"

def write_to_file(data_line):
	"""
    Desc: 
        This file appends a line of data to the output file (writes). This fxn assumes the file has already been open
    Args: 
        data_out_file : This is a reference to the file we are writing data to
        data_line : String array holding the data we are writing to the CSV file 
	Return:
        Nothing
    """

    # open the file
    f = open(data_out_file_name, 'w')

    # init the writer
    writer = csv.writer(f)

    # write the data 
    writer.writerow(data_line)

    # close the file 
    f.close()

	return 


def init_bme280():
    print("\nSparkFun BME280 Sensor Init... \n")
    bme = qwiic_bme280.QwiicBme280()

    if bme.connected == False:
        print("The Qwiic BME280 device isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        quit()

    bme.begin()

    return bme


def query_bme280(bme):
 """
    Desc:
        Query
    """
    #TODO: Check if data is valid. (i.e. length, data values, etc). If invalid return -1

    res = []

    humidity = bme.humidity
    pressure = bme.pressure
    altitude_feet = bme.altitude_feet
    temperature = bme.temperature_fahrenheit

    print("Humidity:\t%.3f" % bme.humidity)
    print("Pressure:\t%.3f" % bme.pressure)    
    print("Altitude:\t%.3f" % bme.altitude_feet)
    print("Temperature:\t%.2f" % bme.temperature_fahrenheit)       
    print("\n")

    res.append(humidity)
    res.append(pressure)
    res.append(altitude_feet)
    res.append(temperature)

    return 



if __name__ == '__main__':
    global bme_obj

    #write the header row 
    write_to_file(header)
    
    #initialize the ICM device
    bme_obj = init_icm20948()

    #Begin inf loop writing data to file.
    while True:
        # fetch icm data. 
        #If -1 returned, data was not fetched and ignore this loop
        bme_data = query_bme280(bme_obj);

        if bme_data == -1
            break
        else    
            #fetch system time
            sys_time = datetime.utcnow().strftime("%Y%m%d%I:%M%p")

            #create string array containing sys time and icm data
            data_row = [sys_time]
            data_row = array.array(sys_time, bme_data)

            #write data row to csv file
            write_to_file(data_row)

        time.sleep(0.1)



# def runExample():

#     print("\nSparkFun BME280 Sensor  Example 1\n")
#     mySensor = qwiic_bme280.QwiicBme280()

#     if mySensor.connected == False:
#         print("The Qwiic BME280 device isn't connected to the system. Please check your connection", \
#             file=sys.stderr)
#         return

#     mySensor.begin()

#     while True:
#         print("Humidity:\t%.3f" % mySensor.humidity)

#         print("Pressure:\t%.3f" % mySensor.pressure)    

#         print("Altitude:\t%.3f" % mySensor.altitude_feet)

#         print("Temperature:\t%.2f" % mySensor.temperature_fahrenheit)       

#         print("")

#         time.sleep(1)


# if __name__ == '__main__':
#     try:
#         runExample()
#     except (KeyboardInterrupt, SystemExit) as exErr:
#         print("\nEnding Example 1")
# sys.exit(0)
