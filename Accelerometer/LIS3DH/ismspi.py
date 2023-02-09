import time
import board
import digitalio
import busio


from adafruit_lsm6ds.ism330dhcx import ISM330DHCX

spi = board.SPI()
cs = digitalio.DigitalInOut(board.D9)
ism330 = ISM330DHCX(spi, cs)

x,y,z = ism.acceleration

print(x, y, z)