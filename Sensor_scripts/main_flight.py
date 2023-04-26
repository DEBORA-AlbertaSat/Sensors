from __future__ import print_function
import time
import sys
import serial
from datetime import datetime, timezone
import csv
import threading

#Import custom python files for each sensor
import gps_collect as gps
import bme280_collect as bme
import icm20948_collect as icm

#This is the main flight program for the DEBORA balloon mission
# All senors are initialized, and data collection loops are ran on seperate threads

# Every sensor thread is checked periodically each __ to ensure it is operating nominally.
#   If not the thread is restarted. 


def write_to_csv_file(data_line, data_out_path):
    # open the file
    f = open(data_out_path, 'a')
    # init the writer
    writer = csv.writer(f)
    # write the data
    writer.writerow(data_line)
    # close the file
    f.close()
    return

class gps_thread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        
    def run(self):
        try:
            serial_obj = gps.init_serial_obj()
            gps.config_gps(serial_obj)
                
        except Exception as e :
            print("Error config GPS Serial:", e)
            
        else:
            write_to_csv_file(gps.gps_header, gps.gps_data_out_file_path)
            
            while True: 
                gps_data = gps.query_gps(serial_obj)
                
                if gps_data != -1:
                    #fetch system time
                    sys_time = datetime.utcnow().strftime("%Y%m%dT%H:%M:%S.%f")

                    #create string array containing sys time and icm data
                    data_row = [sys_time]
                    data_row.extend(gps_data)

                    #write data row to csv file
                    write_to_csv_file(data_row, gps.gps_data_out_file_path)
                    
                time.sleep(0.1)
               
                
class bme_thread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        
    def run(self):
        try:
            bme_obj = bme.init_bme280()
                
        except Exception as e :
            print("Error config bme:", e)
            
        else:
            write_to_csv_file(bme.bme_header, bme.bme_data_out_file_path)
            
            while True: 
                #fetch bme data. 
                #if -1 returned, data was not fetched and ignore this loop
                bme_data = bme.query_bme280(bme_obj)
                
                if bme_data != -1:
                    #fetch system time
                    sys_time = datetime.utcnow().strftime("%Y%m%dT%H:%M:%S.%f")

                    #create string array containing sys time and icm data
                    data_row = [sys_time]
                    data_row.extend(bme_data)

                    #write data row to csv file
                    write_to_csv_file(data_row, bme.bme_data_out_file_path)
                    
                time.sleep(0.1)
                
            
class icm_thread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        
    def run(self):
        try:
            icm_obj = icm.init_icm20948()
                
        except Exception as e :
            print("Error config icm:", e)
            
        else:
            write_to_csv_file(icm.icm_header, icm.icm_data_out_file_path)
            
            while True: 
                #fetch bme data. 
                #if -1 returned, data was not fetched and ignore this loop
                icm_data = icm.query_icm20948(icm_obj)
                
                if icm_data != -1:
                    #fetch system time
                    sys_time = datetime.utcnow().strftime("%Y%m%dT%H:%M:%S.%f")

                    #create string array containing sys time and icm data
                    data_row = [sys_time]
                    data_row.extend(icm_data)

                    #write data row to csv file
                    write_to_csv_file(data_row, icm.icm_data_out_file_path)
                    
                time.sleep(0.1)
                


if __name__ == '__main__':
    print("\nBeginning main flight program... ")

    print("\nCreating sensor threads... ")
    gps_t = gps_thread(1, "GPS thread")
    bme_t = bme_thread(2, "BME thread")
    icm_t = icm_thread(3, "ICM thread")
    
    
    print("\nStarting sensor threads... ")
    gps_t.start()
    bme_t.start()
    icm_t.start()            
        