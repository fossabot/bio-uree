"""BUTTON MODULE
AUTEUR : Luoskate [UPSILON]
DATE : 2018-2019
PROJECT : Bio-Urée
"""

from RPi.GPIO import GPIO
import main


class Button:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(
            pin, GPIO.RISING, callback=main.activated(), bouncetime=200
        )

    def clean(self):
        GPIO.cleanup()
