"""Quick demonstration of the arm"""
import uarm_serial
import serial
conn = serial.serial_for_url("/dev/ttyUSB0")
arm = uarm_serial.uArmSerial(conn)
arm.attach_all()
uarm_serial.go_demo(arm)
