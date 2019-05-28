"""FLOW METER MODULE
AUTEUR : Luoskate [UPSILON]
DATE : 2018-2019
PROJECT : Bio-Urée
"""

import logging
import time

import RPi.GPIO as GPIO

LOGGER = logging.getLogger(f"Bio-Urée.{__name__}")


class Flowmeter:
    def __init__(self, pin):
        self.pin = pin
        self.pulse = 0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=self.pulse_count)

    def pulse_count(self, chn):
        self.pulse += 1

    def check(self, delta_pulse):
        while delta_pulse != 0:
            alpha_pulse = self.pulse
            time.sleep(3)
            delta_pulse = alpha_pulse - self.pulse

    def measure(self, cst):
        LOGGER.debug("Début de mesure du volume d'urine ...")
        self.check(1)
        liters = self.pulse * cst
        self.pulse = 0
        LOGGER.debug(f"Mesure du volume d'urine fini avec {liters} ml")
        return liters

    def clean(self):
        GPIO.cleanup()
