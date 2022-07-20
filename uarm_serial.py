"""uArm python controller.
Requires the uArmSerial code to be running on the arduino.
Usage:

>>> import serial
>>> import uarm_serial
>>> conn = serial.serial_for_url(<portspec>)
>>> arm = uarm_serial.uArmSerial(conn)

You are now connected to the arm.

>>> arm.attach_all()
This will enable all serial motors - it is not the default - you may want to relax
them to save power, or so the open feedack potentiometers can be used as sensors.
See the demo functions at the bottom for examples of movement.
demo_setup is currently configured for my own test machine.
"""

import serial
from functools import partial
import logging

class uArmSerial(object):
    def __init__(self, serial_conn):
        """Params - a connected serial port going to the
        Arduino on the uArm running uARm serial"""
        self._serial_conn = serial_conn
        self._serial_conn.timeout = 0.1
        self.gripper = partial(self._safe_position, 90, 40, 0)
        self.wrist = partial(self._safe_position, 120, 0, 1)
        self.base = partial(self._safe_position, 120, 30, 2)
        self.elbow = partial(self._safe_position, 90, 10, 3)
        self.shoulder = partial(self._safe_position, 110, 30, 4)
        self.clear = True
        #todo determine limits
        #todo - read pots
        #todo cal, and store/read cal data
        self.clear_response()

    def _write_conn(self, data):
        logging.info(data)
        self._serial_conn.write(
            bytes(data, 'utf-8')
            )

#    def decode_lines(self, lines):
#        """Decodes list of utf-8 bytearrays"""
#        lines_decoded
        
    def clear_response(self, force=True):
        if self.clear or force:
            output = self._serial_conn.readlines()
            output = [line.decode('utf-8') for line in output]
            output = ''.join(output)
            if output:
                logging.info( "Flushing...\n%s", output)
                logging.info("Flushed")
        
    def _write_motor(self, motor_number, position):
        """Format a serial string and send it"""
        cmd = "P%d,%d;" % (motor_number, position)
        self._write_conn(cmd)

    def attach(self, joint_no):
        """Attach a servo (power it)"""
        cmd = "A%d;" % (joint_no)
        self._write_conn(cmd)
        self.clear_response()

    def detach(self, joint_no):
        """Detach servo - save power, or become sense only"""
        cmd = "D%d;" % (joint_no)
        self._write_conn(cmd)
        self.clear_response()
        
    def detach_all(self):
        """Detach all - good for record"""
        [self.detach(n) for n in range(5)]

    def attach_all(self):
        [self.attach(n) for n in range(5)]
        
    def read_pot(self, pot_no):
        """Read a potentiometer on the arm"""
        self.clear(force=True)
        cmd = "?%d;" % (pot_no)
        self._write_conn(cmd)
        response = ''.join(self._serial_conn.readlines()).decode('utf-8')
        logging.info(response)
        response = response[1].strip()
        return int(response)
        
    def _safe_position(self, high, low, motor_no, position):
        assert low <= position <= high
        self._write_motor(motor_no, position)
        
import time

def go_demo(arm):
    arm.gripper(40)
    arm.shoulder(90)
    arm.elbow(90)
    time.sleep(1)
    arm.shoulder(30)
    arm.elbow(60)
    time.sleep(1)
    arm.gripper(90)
    time.sleep(1)
    arm.shoulder(90)
    time.sleep(0.4)
    arm.elbow(90)
    

def demo_setup():
    logging.basicConfig(level=logging.INFO)
    import platform
    if 'linux' in platform.platform().lower():
        conn = serial.serial_for_url("/dev/ttyUSB0")
        conn.baudrate = 9600
    else:
        conn = serial.serial_for_url("COM4:9600")
    conn.timeout = 0.1
    found_ready = False
    while not found_ready:
        data = [line.decode('utf-8') for line in conn.readlines()]
        data = ''.join(data)
        found_ready = 'Ready' in data
        if data:
            print(data)
    
    arm = uArmSerial(conn)
    arm.attach_all()
    arm.wrist(87)
    arm.clear = False
    go_demo(arm)
    conn.close()
    

# demo_setup()
# import time
# 
# try:
#     arm = uArmSerial(conn)
#     while True:
#         logging.info( [arm.read_pot(n) for n in range(5)])
#         time.sleep(0.1)
#    arm.gripper(10)
#    time.sleep(1)
#    arm.gripper(80)
#    arm.read_pot(0)
# finally:
#     conn.close()
