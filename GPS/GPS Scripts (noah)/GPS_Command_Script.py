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

HEX = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']

Begin = "$PTNLSRT,F,,35*"
End = "\r\n"
MSB = 0
LSB = 0
# Is a brute force way to send commands since the ending 2 digits need to be a special combination
#for each command, and I'm currently unable to find out to calculate it
for MSB in range(16):
    LSB = 0
    for LSB in range(16):
        msg = Begin + HEX[MSB] + HEX[LSB] + End
        msg = bytes(msg,'utf-8')
        ser.write(msg)
        LSB = LSB + 1
        time.sleep(0.2)
    MSB = MSB + 1
print("DONE")
