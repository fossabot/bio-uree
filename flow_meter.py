"""FLOW METER MODULE
AUTEUR : Luoskate [UPSILON]
DATE : 2018-2019
PROJECT : Bio-Urée
"""

import time

import RPi.GPIO as GPIO


class Flowmeter:
    def __init__(self, pin):
        self.pin = pin
        self.pulse = 0
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def pulse_count(self, pin):
        self.pulse += 1

    def check(self, delta_pulse):
        while delta_pulse != 0:
            alpha_pulse = self.pulse
            time.sleep(1)
            delta_pulse = alpha_pulse - self.pulse

    def measure(self, cst):
        GPIO.add_event_detect(
            self.pin, GPIO.FALLING, callback=self.pulse_count(self.pin), bouncetime=10
        )
        self.check(1)
        liters = self.pulse * cst
        GPIO.remove_event_detect(self.pin)
        self.pulse = 0
        return liters

    def clean(self):
        GPIO.cleanup()
