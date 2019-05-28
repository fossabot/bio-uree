import RPi.GPIO as GPIO
import time
import random

button_pin = 21
lv_pin = 27
flowmeter_pin = 20

# change this variable for other flow streams
# 1.0  == 0.135 l/m
# 5.0  == 0.675 l/m
# 10.0 == 1.35  l/m
# 20.0 == 2.7   l/m
frequency = 1

seconds = 1 / (2 * frequency)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(flowmeter_pin, GPIO.OUT)
GPIO.setup(button_pin, GPIO.OUT)
GPIO.setup(lv_pin, GPIO.OUT)

GPIO.output(button_pin, False)
GPIO.output(flowmeter_pin, False)
GPIO.output(lv_pin, False)

try:
    GPIO.output(button_pin, True)
    GPIO.output(button_pin, False)
    for i in range(25):
        GPIO.output(flowmeter_pin, False)
        time.sleep(seconds)
        GPIO.output(flowmeter_pin, True)
        time.sleep(seconds)

except KeyboardInterrupt:
    GPIO.cleanup()