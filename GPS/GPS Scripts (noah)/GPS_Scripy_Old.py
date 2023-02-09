import time
import serial

ser = serial.Serial(
    port = '/dev/ttyS0',
    baudrate = 4800,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1
)

while 1:
    msg = (str)(ser.readline())
    print(msg)