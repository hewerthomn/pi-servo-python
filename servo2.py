# RS_Servo.py - Wrapper Servo Class for Raspberry Pi
#
# 15 February 2017 - 1.0 Original Issue
# 18 February 2017 - 1.1 Modified with @property
#
# Reefwing Software

import RPi.GPIO as GPIO
from time import sleep

# Private Attributes
__CALIBRATE      = 1
__SET_DUTY_CYCLE = 2
__SCAN           = 3
__QUIT           = "q"

class Servo:
    # Servo class wrapper using RPi.GPIO PWM

    # Servo private class attribute - to count servo instances
    __number = 0

    def __init__(self, pin, min_dc=3, max_dc=13, freq=50):
        # Create a new servo instance with default pulse width limits if not provided

        # Configure the Pi to use pin names (i.e. BCM) and allocate I/O
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)

        # Create PWM channel on the servo pin with a frequency of freq - default 50Hz
        self.PWM = GPIO.PWM(pin, freq)

        # Increment Servo instances
        self.__number += 1     
        
        # Instance attributes
        self.pin = pin
        self.min_duty_cycle = min_dc
        self.max_duty_cycle = max_dc
        self.duty_cycle = self.get_centre(min_dc, max_dc)
        self.angle = 0

    def __str__(self):
        # Return string representation of servo
        return "Servo: pin - {0}, MIN_DC - {1}, MAX_DC - {2}, DC - {3}".format(self.pin, self.min_duty_cycle, self.max_duty_cycle, self.duty_cycle)

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
        # Scans from min_dc to max_dc - defaults to max and min duty cycle
	min_dc = self.min_duty_cycle
	max_dc = self.max_duty_cycle
        centre = self.get_centre(min_dc, max_dc)

	dc = min_dc
        self.duty_cycle = dc
	self.cal_duty_cycle = dc
	print("dc", dc)
        sleep(1)

	dc = centre
        self.duty_cycle = dc
	self.cal_duty_cycle = dc
	print("dc2", dc)
        sleep(1)

        self.duty_cycle = max_dc
	print("dc3", self.duty_cycle)
        sleep(1)
        self.duty_cycle = centre
	print("dc4", self.duty_cycle)
        sleep(1)

    def cal_duty_cycle(self, dc):
        # Set duty cycle for servo - not clamped
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
	print("duty cycle setter")

    @staticmethod
    def get_centre(min_dc, max_dc):
         return min_dc + (max_dc - min_dc)/2

    @staticmethod
    def clamp(dc, min_dc, max_dc):
        return max(min(dc, max_dc), min_dc)
    
    @classmethod
    def count(cls):
        # Returns the number of Servo instances
        return cls.__number

def main():
    servo = Servo(17)

    try:
        servo.start()       # start PWM for servo

        print(servo)
        print("Servo instances: ", Servo.count())

        while True:
            test = input("\nSelect Action - (1) Calibrate, (2) Set max/min duty cycle, or (3) Scan: ")

            if test == __CALIBRATE:
                while True:
                    response = raw_input("Enter Duty Cycle (q = quit):")
                    if response == __QUIT:
                        break;
                    servo.cal_duty_cycle(float(response))
            elif test == __SET_DUTY_CYCLE:
                min_dc = float(input("Enter minimum duty cycle: "))
                max_dc = float(input("Enter maximum duty cycle: "))
                servo.min_duty_cycle = min_dc
                servo.max_duty_cycle = max_dc
                print(servo)
            else:
                while True:
                    # Scan Servo from min duty cycle to max duty cycle
                    print("\nScanning (CTRL c to exit)...")
                    servo.scan()
    except KeyboardInterrupt:
        print("\n-- CTRL-C: Terminating program --")
    finally:
        print("Cleaning up PWM and GPIO...")
        servo.cleanup()
        GPIO.cleanup()
        print("Done.")

if __name__ == "__main__":
    # execute only if run as a script
    main()
