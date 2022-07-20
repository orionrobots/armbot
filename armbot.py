import serial
import smbus2
import time

from uarm_serial import uArmSerial, go_demo
from md25_rpi_i2c import Md25pi

class Robot:
    def __init__(self, serial_port_spec='/dev/ttyUSB0', md25_bus=1, md25_address=0x58):
        ser_conn = serial.serial_for_url(serial_port_spec)
        self.arm = uArmSerial(ser_conn)
        self.bus = smbus2.SMBus(md25_bus)
        self.motors = Md25pi(self.bus, md25_address)

    def close(self):
        self.bus.close()

    def move(self, speed, rotation=0, for_time=0.1):
        left = speed + 128 + rotation
        right = speed + 128 - rotation
        with self.motors.safe():
            self.motors.set_left(left)
            self.motors.set_right(right)
            time.sleep(for_time)

    def go_arm(self):
        go_demo(self.arm)

    def turn_left(self, speed=80, for_time=0.4):
        self.move(speed, -128, for_time)

    def turn_right(self, speed=80, for_time=0.4):
        self.move(speed, 128, for_time)

    def forward(self, speed=80, for_time=0.8):
        self.move(speed, 0, for_time)
    
    def backwards(self, speed=80, for_time=0.8):
        self.forward(speed=-speed, for_time=for_time)
