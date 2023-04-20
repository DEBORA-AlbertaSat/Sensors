from __future__ import print_function
import qwiic_icm20948
import time
import sys

import csv
 
from datetime import datetime, timezone

# Accelerometer is measured in milli G's (G forces = m/s^2) [mg]
# Gyroscope is measured in Degrees per second [DPS]
# Magnetometer is measured in micro Teslas
header = ["SysTime [UTC]", "Ax [mg]", "Ay [mg]", "Az [mg]", "Gx [DPS]","Gy [DPS]", "Gz [DPS]", "Mx [uT]", "My [uT]", "Mz [uT]" ] 

data_out_file_name = "/home/albertasat/DEBORA/Sensors/Data/icm20948_data/test_data.csv"


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


def init_icm20948():
    print("\nSparkFun 9DoF ICM-20948 Sensor Init... \n")
    icm = qwiic_icm20948.QwiicIcm20948()
    if icm.connected == False:
        print("The Qwiic ICM20948 device isn't connected to the system. Please check your connection", \
            file=sys.stderr)
        quit()
    icm.begin()
    return icm


def query_icm20948(icm_obj):
    #TODO: Check if icm data is valid. (i.e. length, data values, etc). If invalid return -1
    res = []

    if icm_obj.dataReady():
        icm_obj.getAgmt() # reads all axis data
        res.append('{: 06d}'.format(icm_obj.axRaw))
        res.append('{: 06d}'.format(icm_obj.ayRaw))
        res.append('{: 06d}'.format(icm_obj.azRaw))
        res.append('{: 06d}'.format(icm_obj.gxRaw))
        res.append('{: 06d}'.format(icm_obj.gyRaw))
        res.append('{: 06d}'.format(icm_obj.gzRaw))
        res.append('{: 06d}'.format(icm_obj.mxRaw))
        res.append('{: 06d}'.format(icm_obj.myRaw))
        res.append('{: 06d}'.format(icm_obj.mzRaw))
        
        return res 

    else:
        return -1


if __name__ == '__main__':
    #write the header row 
    write_to_file(header)
    
    #initialize the ICM device
    icm_obj = init_icm20948()

    print("\nBeginning data collection... \n")
    #Begin inf loop writing data to file.
    while True:
        # fetch icm data. 
        #If -1 returned, data was not fetched and ignore this loop
        icm_data = query_icm20948(icm_obj)

        if icm_data == -1:
            continue
        else:    
            #fetch system time
            sys_time = datetime.utcnow().strftime("%Y%m%dT%H:%M:%S.%f")

            #create string array containing sys time and icm data
            data_row = [sys_time]
            data_row.extend(icm_data)

            #write data row to csv file
            write_to_file(data_row)

        time.sleep(0.1)

    
