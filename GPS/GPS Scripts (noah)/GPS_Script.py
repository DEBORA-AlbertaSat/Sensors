import time
import serial
import datetime

Date = str(datetime.date.today())
File_Name = "GPS_Data_" + Date + ".txt"

ser = serial.Serial(
        port = '/dev/ttyS0',
        baudrate = 4800,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS,
        timeout = 1
        )

while 1:
        Data = str(ser.readline())
        
        with open(File_Name, 'a', encoding = 'utf-8') as GPS_File:
            
            GPS_File.writelines(Data + '\n')
            print(Data)
            time.sleep(0.1)
        