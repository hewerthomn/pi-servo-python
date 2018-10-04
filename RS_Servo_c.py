# RS_Servo.py - Wrapper Servo Class for Raspberry Pi
#
# 15 February 2017 - 1.0 Original Issue
# 18 February 2017 - 1.1 Modified with @property
#
# Reefwing Software

import RPi.GPIO as GPIO
from time import sleep

# Private Attributes
__CALIBRATE	 = "1"
__SET_DUTY_CYCLE = "2"
__SCAN		 = "3"
__QUIT		 = "q"

class Servo:
	# Servo class wrapper using RPi.GPIO PWM

	# Servo private class attribute - to count servo instances
	__number = 0

	def __init__(self, pin, min_dc=2, max_dc=10, freq=50):
		# Create a new servo instance with default pulse width limits if not provided

		# Configure the Pi to use pin names (i.e. BCM) and allocate I/O
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(pin, GPIO.OUT)

		# Create PWM channel on the servo pin with a frequency of freq
		# default 50Hz
		self.PWM = GPIO.PWM(pin, freq)

		# Increase Servo Instace
		type(self).__number += 1

		# Instance attributes
		self.pin = pin
		self.min_duty_cycle = min_dc
		self.max_duty_cycle = max_dc
		self.duty_cycle = self.get_centre(min_dc, max_dc)
		self.angle = 0

	def __str__(self):
		# Return string representation of servo
		return "Servo: pin: {0}, MIN_DC: {1}, MAX_DC: {2}, DC: {3}".format(self.pin, self.min_duty_cycle, self.max_duty_cycle, self.duty_cycle)

	def start(self):
		# Start PWM
		self.PWM.start(self.duty_cycle)

	def stop(self):
		# Stop PWM
		self.PWM.stop()

	def centre(self):
		# Move servo to the centre position
		centre = self.get_centre(self.min_duty_cycle, self.max_duty_cycle)
		self.duty_cycle = centre

	def min_dc(self):
		# Move servo to minimum duty cycle position
		self.duty_cycle = self.min_duty_cycle

	def max_dc(self):
		# Move servo to maximum duty cycle position
		self.duty_cycle = self.max_duty_cycle

	def scan(self, min_dc=None, max_dc=None):
		# Scans from min_dc to max_dc -defaults to max and min duty cycle
		min_dc = (min_dc or self.min_duty_cycle)
		max_dc = (max_dc or self.max_duty_cycle)
		centre = self.get_centre(min_dc, max_dc)
		self.duty_cycle =  min_dc
		sleep(1)
		self.duty_cycle = centre
		sleep(1)
		self.duty_cycle = max_dc
		sleep(1)
		self.duty_cycle = centre
		sleep(1)

	def cal_duty_cycle(self, dc):
		# Set duty cycle for servo - not campled
		self.PWM.ChangeDutyCycle(dc)

	def cleanup(self):
		# Stop PWM channel for servo and centre
		self.centre()
		sleep(1)
		self.stop()
	

	@property
	def duty_cycle(self):
		return self.__duty_cycle

	@duty_cycle.setter
	def duty_cycle(self, dc):
		# Set duty cycle for servo - clamped to max and min duty cycle
		dc = self.clamp(dc, self.min_duty_cycle, self.max_duty_cycle)
		self.PWM.ChangeDutyCycle(dc)
		self.__duty_cycle = dc

	@staticmethod
	def get_centre(min_dc, max_dc):
		return min_dc + (max_dc - min_dc) / 2

	@staticmethod
	def clamp(dc, min_dc, max_dc):
		return max(min(dc, max_dc), min_dc)

	@classmethod
	def count(cls):
		return cls.__number


