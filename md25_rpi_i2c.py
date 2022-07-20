import smbus2
from contextlib import contextmanager

MD25_SPEED1 = 0
MD25_SPEED2 = 1
MD25_TURN = 1
MD25_ENC1A = 2
MD25_ENC1B = 3
MD25_ENC1C = 4
MD25_ENC1D = 5
MD25_ENC2A = 6
MD25_ENC2B = 7
MD25_ENC2C = 8
MD25_ENC2D = 9
MD25_BATTV = 10
MD25_M1_CRNT = 11
MD25_M2_CRNT = 12
MD25_SW_REV = 13
MD25_ACC = 14
MD25_MODE = 15
MD25_COMMAND = 16

class Md25pi:
        def __init__(self, bus, address):
                self._bus = bus
                self._address = address

        def write_byte(self, register, byte):
                """Write a single data byte to a register"""
                self._bus.write_byte_data(self._address, register, byte)

        def read_register(self, register):
                """Write a single register byte"""
                return self._bus.read_byte_data(self._address, register)
        def get_version(self):
                """Get device version number"""
                return self.read_register(MD25_SW_REV)

        def get_battery_volts(self):
                """Get the battery voltage"""
                return self.read_register(MD25_BATTV)/10
        
        def stop(self):
                """Stop all movement"""
                self.write_byte(MD25_SPEED1, 128)
                self.write_byte(MD25_SPEED2, 128)

        def set_left(self, speed):
                """Start left motor. Speed +/- 127"""
                self.write_byte(MD25_SPEED2, 128 - speed)

        def set_right(self, speed):
                """Start left motor. Speed +/- 127"""
                self.write_byte(MD25_SPEED1, 128 - speed)

	def read_left_encoder(self):
		"""Read the 4 encoder registers, return an int"""
		return [
		  self._bus.read_register(self._address, MD25_ENC1A),
		  self._bus.read_register(self._address, MD25_ENC1B),
                  self._bus.read_register(self._address, MD25_ENC1C),
                  self._bus.read_register(self._address, MD25_ENC1D)]

	def read_right_encoder(self):
		"""Read the 4 encoder registers, return an int"""
		return [
		  self._bus.read_register(self._address, MD25_ENC2A),
                  self._bus.read_register(self._address, MD25_ENC2B),
                  self._bus.read_register(self._address, MD25_ENC2C),
                  self._bus.read_register(self._address, MD25_ENC2D)]

        @contextmanager
        def safe(self):
                try:
                        yield self
                finally:
                        self.stop()

def main():
        import time
        address = 0x58
        bus = smbus.SMBus(1)
        motors = Md25pi(bus, address)
        try:
                print("Version is ", motors.get_version())
                print("Battery voltage is ", motors.get_battery_volts())
                assert motors.get_battery_volts() >= 80, "Too low - did you turn it on?"
                motors.set_left(70)
                motors.set_right(70)
                time.sleep(1)
                motors.set_left(50)
                time.sleep(1)
                motors.set_left(70)
                motors.set_right(70)
                time.sleep(1)
        finally:
                motors.stop()

if __name__ == '__main__':
        main()
