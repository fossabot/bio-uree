import RPi.GPIO as GPIO
import time

flowmeter_pin = 20
button_pin = 21

# change this variable for other flow streams
# 1.0  == 0.135 l/m
# 5.0  == 0.675 l/m
# 10.0 == 1.35  l/m
# 20.0 == 2.7   l/m
frequency = 4

seconds = 1 / (2 * frequency)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(button_pin, GPIO.OUT)
GPIO.setup(flowmeter_pin, GPIO.OUT)

GPIO.output(button_pin, False)
GPIO.output(flowmeter_pin, False)
try:
    GPIO.output(button_pin, True)
    GPIO.output(button_pin, False)
    time.sleep(1)
    for i in range(20):
        GPIO.output(flowmeter_pin, True)
        print("pulse ", i)
        time.sleep(seconds)
        GPIO.output(flowmeter_pin, False)
        time.sleep(seconds)

except KeyboardInterrupt:
    GPIO.cleanup()

