# This python script is used to configure and send commands to the Copernicus II GPS Module
#
# Refer to the documntation for NMEA message format for commands
#
# The input and output of each message is in NMEA 0183 format (you can read more in the last
# chapter of the Copernicus II documentation)
#
# ** Important note: Each command must be accompanied with a two digit hex checksum. It's not that
# intuitive to understand how to find this but basically you need to convert each character of a 
# command/message '$' and '*' from ascii into hex. Then, consecutively XOR the lower half bytes (nibble).
# Do the same for the upper half byte. The result of both these operations is the checksum.
#
# Example 1: "$PTNLSKG,,,*" => 0x24 0x50 0x54 0x4E 0x4C 0x53 0x4B 0x47 0x2C 0x2C 0x2C 0x2A 
#	Lower Half Byte XOR = 4 XOR 0 XOR 4 XOR E XOR C XOR ... = 5
#	Upper Half Byte XOR = 2 XOR 5 XOR 5 XOR 4 XOR 4 XOR ... = 7
#	=> 0x75 = Checksum
#
#	So the command here would be $PTNLSKG,,,*75
#

import time
import serial

# INPUT COMMAND INSIDE QUOTATIONS (no spaces). Command is sent 1 seconds after script is run
command = "$PTNLQBA*54"

# Here are some common commands (with their checksums calculated):
#
# Check Antenna Status (connected/disconnected) - REQUIRES a ANTENNA DETECTION CIRCUIT TO WORK: $PTNLQBA*54
#
# Set GPS Receiver to AIR mode: $PTNLSCR,,,,,,,3,,*5B
# Set GPS Receiver to LAND mode: $PTNLSCR,,,,,,,1,,*59
#
# Check GPS Receiver Sensitivity mode: $PTNLQFS*42
# Set GPS Receiver Sensitivity to High: $PTNLSFS,H,0*38
# Set GPS Receiver Sensitivity to Standard: $PTNLSFS,S,0*23
#
# Set GPS initial location to ~ UofA Varsity Field: $PTNLSKG,,,5331.45390,N,11331.77150,W,*56
# Set GPS initial location to ~ UofA South Campus: $PTNLSKG,,,5330.31670,N,11331.83670,W,*51
#
# Reset GPS (Factory reset, Erases almanac, ephemeris, last position in flash SRAM: $PTNLSRT,F,4,,*21
#

ser = serial.Serial(
    port = '/dev/ttyS0',
    baudrate = 4800,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 1
)

time.sleep(0.7)
txData = command + "\r\n"
# while(1):	# **** Optional if want continous responses and intermittent transmission (of same message)
ser.write(txData.encode())
print ("\033[1mTransmitted Command: " + command + "\033[0m")

# Feeds a couple of Rx transmissions mainly to see the response/acknowledgement of the command from the GPS receiver
for count in range(10):
	Data = ser.readline().decode()
	print (Data)

time.sleep(1)
exit()
