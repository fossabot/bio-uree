"""RELAIS MODULE
AUTEUR : Luoskate [UPSILON]
DATE : 2018-2019
PROJECT : Bio-Urée
"""

from RPi.GPIO import GPIO


class Relais:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

    def activate(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def desactivate(self):
        GPIO.output(self.pin, GPIO.LOW)

    def clean(self):
        GPIO.output(self.pin, GPIO.LOW)
        GPIO.cleanup()
