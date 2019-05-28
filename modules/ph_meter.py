import sys
import time

from modules.DFRobot_ADS1115 import ADS1115
from modules.DFRobot_PH import DFRobot_PH

ADS1115_REG_CONFIG_PGA_6_144V = 0x00  # 6.144V range = Gain 2/3
ADS1115_REG_CONFIG_PGA_4_096V = 0x02  # 4.096V range = Gain 1
ADS1115_REG_CONFIG_PGA_2_048V = 0x04  # 2.048V range = Gain 2 (default)
ADS1115_REG_CONFIG_PGA_1_024V = 0x06  # 1.024V range = Gain 4
ADS1115_REG_CONFIG_PGA_0_512V = 0x08  # 0.512V range = Gain 8
ADS1115_REG_CONFIG_PGA_0_256V = 0x0A  # 0.256V range = Gain 16


class PhMeter:
    def __init__(self, pin):
        self.ads1115 = ADS1115()
        self.ph = DFRobot_PH()
        self.ph.begin()
        # Set the IIC address
        self.ads1115.setAddr_ADS1115(0x48)
        # Sets the gain and input voltage range.
        self.ads1115.setGain(ADS1115_REG_CONFIG_PGA_6_144V)

    def calibrate(self):
        # Get the Digital Value of Analog of selected channel
        adc0 = self.ads1115.readVoltage(0)
        print(adc0)
        print("A0:%dmV " % (adc0["r"]))
        # Calibrate the calibration data
        return self.ph.calibration(adc0["r"])

    def read(self):
        # Read your temperature sensor to execute temperature compensation
        temperature = 25
        # Get the Digital Value of Analog of selected channel
        adc0 = self.ads1115.readVoltage(0)
        print(adc0)
        # Convert voltage to PH with temperature compensation
        _ph = self.ph.readPH(adc0["r"], temperature)
        print(_ph)
        print("Temperature:%.1f ^C PH:%.2f" % (temperature, _ph))
        return _ph

    def reset(self):
        self.ph.reset()
