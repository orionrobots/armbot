import serial
import smbus2

from uarm_serial import uArmSerial
from md25_rpi_i2c import Md25pi

class Robot:
    def __init__(self, serial_port_spec='/dev/ttyUSB0:9600', md25_bus=1, md25_address=0x58):
        ser_conn = serial.serial_for_url(serial_port_spec)
        self.arm = uArmSerial(ser_conn)
        self.bus = smbus2.SMBus(md25_bus)
        self.motors = Md25pi(self.bus, md25_address)

    def close(self):
        self.bus.close()
