# Armbot

ArmBot is a robot combining the uFactory uArm 4 DOF robot arm, with the MD25 motor controller and chassis I previously used for the eeebot.

See this robot at https://www.youtube.com/watch?v=xY6Oc4_jdmU&ab_channel=Orionrobots

Here are all the code components that I am using to get the robot moving. All python code is python3 unless otherwise stated. The intent is that it will all run on the Raspberry Pi.

* uArm_serial -> Arduino project needed to set up the arm for control from python
* uarm_serial.py -> Python library for moving the arm, including demonstration functions.

## Arm hardware

* md25/rd01 robot drive system with:
 * Big beefy motors and wheels
 * Built in encoders - relative position and speed
 * Dual h-bridge controller, with built in voltage regulator, and i2c/serial interface. High level speed and encoder interfaces.
* eeeBot chassis - the above mounted along with 8 aa batteries, a power switch and a furniture castor at the front.
* uArm - a 4 DOF servo controlled arm with an arduino Uno, open feedback servo's, user input tac switches and a beeper.
* Raspberry Pi (model 3b+ or later)
* Raspberry Pi camera
* Phone backup battery supply (for logic)

## Installation on raspbian

* apt-get install i2ctools, python-smbus, python-pip, 
* i2c kernel config (raspi config)
* Everything here - https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c

## Notes for computer vision

This is roadmapped - not yet part of this code.

vision -
setup picamera
then python-opencv, python-numpy
python-scipy

