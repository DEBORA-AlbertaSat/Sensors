import time
import board
from adafruit_lsm6ds.lsm6ds import LSM6DS

i2c = board.I2C()

sensor = LSM6DS(i2c)

while True:
      print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2" % (sensor.acceleration))
      print("Gyro X:%.2f, Y: %.2f, Z: %.2f radians/s" % (sensor.gyro))
      print("")
      time.sleep(0.5)

