import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnigs(False)

GPIO.setup(5, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)

GPIO.output(5, 1)
GPIO.output(7, 0)
GPIO.output(11, 1)
GPIO.output(13, 0)

time.sleep(3)

GPIO.output(5, 0)
GPIO.output(7, 1)
GPIO.output(11, 0)
GPIO.output(13, 1)

time.sleep(3)

GPIO.output(5, 0)
GPIO.output(7, 0)
GPIO.output(11, 0)
GPIO.output(13, 0)

