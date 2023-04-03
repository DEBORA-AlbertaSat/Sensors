
from __future__ import print_function
import qwiic_bme280
import time
import sys

import csv

import array

from datetime import datetime, timezone

header = ["SysTime, Humidity, Pressure, Altitude [m], Temperature [C]"]

data_out_file_name = "/home/albertasat/DEBORA/Sensors/Data/bme280_data/test_data.csv"

def write_to_file(data_line):

    # open the file
    f = open(data_out_file_name, 'a')

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

    #TODO: Check if data is valid. (i.e. length, data values, etc). If invalid return -1

    res = []

    humidity = bme.humidity
    pressure = bme.pressure
    altitude = bme.altitude_meters
    temperature = bme.temperature_celsius

    print("Humidity:\t%.3f" % humidity)
    print("Pressure:\t%.3f" % pressure)    
    print("Altitude:\t%.3f" % altitude)
    print("Temperature:\t%.2f" % temperature)       
    print("\n")

    res.append(humidity)
    res.append(pressure)
    res.append(altitude)
    res.append(temperature)

    return res



if __name__ == '__main__':
    global bme_obj

    #write the header row 
    write_to_file(header)
    
    #initialize the ICM device
    bme_obj = init_bme280()

    #Begin inf loop writing data to file.
    while True:

        # fetch icm data. 
        #If -1 returned, data was not fetched and ignore this loop
        bme_data = query_bme280(bme_obj);

        print(bme_data)

        if bme_data == -1:
            break
        else:
            
            #fetch system time
            sys_time = datetime.utcnow().strftime("%Y%m%dT%H:%M:%S.%f")


            # sys_time = "TESTS"

            #create string array containing sys time and icm data
            data_row = [sys_time]
            data_row.extend(bme_data)

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
