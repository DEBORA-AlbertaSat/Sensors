from __future__ import print_function
import qwiic_bme280
import time
import sys

import csv

from datetime import datetime, timezone

# Altitude is not an exact value. It is calculated from barometric pressure and is instead an equivalent value
bme_header = ["SysTime [UTC], Humidity [%RH], Pressure [Pa], Altitude [m], Temperature [C]"]

bme_data_out_file_path = "/home/albertasat/DEBORA/Sensors/Data/bme280_data/bme_data.csv"

def write_to_file(data_line):
    # open the file
    f = open(bme_data_out_file_path, 'a')
    # init the writer
    writer = csv.writer(f)
    # write the data 
    writer.writerow(data_line)
    # close the file 
    f.close()
    return 


def init_bme280():
    print("\nSparkFun BME280 Sensor Init ")
    bme = qwiic_bme280.QwiicBme280()
    if bme.connected == False:
        print("The Qwiic BME280 device isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        quit()
    bme.begin()

    #Ensure this matches the current location's pressure (hPa) at sea level
    bme.sea_level_pressure = 1013.25

    return bme


def query_bme280(bme):
    #TODO: Check if data is valid. (i.e. length, data values, etc). If invalid return -1
    res = []

    try:
        humidity = bme.humidity
        pressure = bme.pressure
        altitude = bme.altitude_meters
        temperature = bme.temperature_celsius

        #FOR DEBUG
        # print("Humidity:\t%.3f" % humidity)
        # print("Pressure:\t%.3f" % pressure)    
        # print("Altitude:\t%.3f" % altitude)
        # print("Temperature:\t%.2f" % temperature)       
        # print("\n")

        res.append(humidity)
        res.append(pressure)
        res.append(altitude)
        res.append(temperature)
        
        if len(res) == 4:
            return res
        
        return -1
            
    except Exception as e:
        print("BME data read error: ", e)
        time.sleep(10)
        return -1


if __name__ == '__main__':
    #write the header row 
    write_to_file(bme_header)
    
    #initialize the ICM device
    bme_obj = init_bme280()

    print("\nBeginning data collection... \n")
    #Begin inf loop writing data to file.
    while True:
        #fetch bme data. 
        #if -1 returned, data was not fetched and ignore this loop
        bme_data = query_bme280(bme_obj)

        if bme_data == -1:
            continue
        else:
            #fetch system time
            sys_time = datetime.utcnow().strftime("%Y%m%dT%H:%M:%S.%f")

            #create string array containing sys time and icm data
            data_row = [sys_time]
            data_row.extend(bme_data)

            #write data row to csv file
            write_to_file(data_row)

        time.sleep(0.1)
