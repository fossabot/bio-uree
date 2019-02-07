"""LEVEL SENSOR MODULE
AUTEUR : Luoskate [UPSILON]
DATE : 2018-2019
PROJECT : Bio-Urée
"""

import RPi.GPIO as GPIO


class lv_sensor:
    def __init__(self, pin, callback):
        self.pin = pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.IN)
        GPIO.add_event_detect(pin, GPIO.RISING, callback=callback, bouncetime=200)

    def clean(self):
        GPIO.cleanup()
