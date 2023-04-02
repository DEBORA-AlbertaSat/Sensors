from __future__ import print_function
import qwiic_icm20948
import time
import sys

import csv
 
from datetime import datetime, timezone

import array

header = ["SysTime", "Ax", "Ay", "Az", "Gx","Gy", "Gz", "Mx", "My", "Mz"] 

data_out_file_name = "~/DEBORA/Sensors/Data/icm20948_data"


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


def init_icm20948():
    """
    Desc:
        Initialize the icm sensor object using associated qwiic library methods.
        If the device is not recognized by the pi, then the program quits.

    Returns:
        Initialized ICM_20958 object 
    """

    print("\nSparkFun 9DoF ICM-20948 Sensor Init... \n")

	icm = qwiic_icm20948.QwiicIcm20948()

	if icm.connected == False:
		print("The Qwiic ICM20948 device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		quit()

	icm.begin()

    return icm


def query_icm20948(icm_obj):
    """
    Desc:
        Queries the icm on the i2c bus and returns an array of accelerometer axis values.
        If the icm does not have data ready, it returns -1 instead
    """
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

    else
        return -1


if __name__ == '__main__':
    global icm_obj

    #write the header row 
    write_to_file(header)
    
    #initialize the ICM device
    icm_obj = init_icm20948()

    #Begin inf loop writing data to file.
    while True:
        # fetch icm data. 
        #If -1 returned, data was not fetched and ignore this loop
        icm_data = query_icm20948(icm_obj);

        if icm_data == -1
            break
        else    
            #fetch system time
            sys_time = datetime.utcnow().strftime("%Y%m%d%I:%M%p")

            #create string array containing sys time and icm data
            data_row = [sys_time]
            data_row = array.array(sys_time, icm_data)

            #write data row to csv file
            write_to_file(data_row)

        time.sleep(0.1)

    
