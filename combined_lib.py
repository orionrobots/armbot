import md25_rpi_i2c as md25
import uarm_serial
import serial
import time

class ArmBot(object):
  def __init__(self, md25_addr=0x58, bus_addr=1, portspec="/dev/ttyUSB0"):
    bus = md25.smbus.SMBus(bus_addr)
    self.motors = md25.Md25pi(bus, md25_addr)
    conn = serial.serial_for_url(portspec)
    conn.baudrate = 9600
    self.arm = uarm_serial.uArmSerial(conn)

  def go_arm(self):
    uarm_serial.go_demo(self.arm)

  def forward(self, speed=80, for_ms=0.8):
    try:
      self.motors.set_left(speed)
      self.motors.set_right(speed)
      time.sleep(for_ms)
    finally:
      self.motors.stop()

  def backwards(self, speed=80, for_ms=0.8):  
    self.forward(speed=-speed, for_ms=for_ms)

  def turn_left(self, speed=80, for_ms=0.4):
    try:
      self.motors.set_left(speed);
      self.motors.set_right(-speed);
      time.sleep(for_ms)
    finally:
      self.motors.stop()

  def turn_right(self, speed=80, for_ms=0.4):
    self.turn_left(-speed)

