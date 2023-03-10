from lis3dh import LIS3DH, device
from time import sleep

registers = device()
lis = LIS3DH(port=1, scale=registers.CTRL_REG4.SCALE_4G, data_rate=registers.CTRL_REG1.ODR_10Hz)

data = lis.read_dummy_register()
print("DUMMY REG CHECK ERROR: " + str(data)) # 0: No Error, -1: Error

lis.enable_axes(registers.CTRL_REG1.Xen | registers.CTRL_REG1.Yen | registers.CTRL_REG1.Zen)

while lis.read_data_ready_register() == lis.ERROR:
    sleep(0.25)

data = lis.read_all_axes()
print("x(g): {}, y(g): {}, z(g): {}".format(data[0], data[1], data[2]))
