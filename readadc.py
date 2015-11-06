#!/usr/bin/env python

################################################################
# Script:     readadc.py
# Author:     ? (Someone at Adafruit, I think), mods: Jeff VanSickle
# Created:    20151028
# Modified:   20151028
#
# Script reads data in from 3008 ADC, which itself is reading
# from an analog temperature sensor (TMP36). Effing balls, the
# conventions in this code are awful; cleaned those up right
# away.
#
# UPDATES:
#     yyyymmdd JV - Changed something, commenting here
#
# INSTRUCTIONS:
#
################################################################

import RPi.GPIO as GPIO

# MCP3008 to RasPi Pin connections
class PINS:
    SPICLK = 5 #18
    SPIMISO = 6 #23
    SPIMOSI = 13 #24
    SPICS = 19 #25


 # Set up the SPI interface pins
def initialize():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(PINS.SPIMOSI, GPIO.OUT)
    GPIO.setup(PINS.SPIMISO, GPIO.IN)
    GPIO.setup(PINS.SPICLK, GPIO.OUT)
    GPIO.setup(PINS.SPICS, GPIO.OUT)


# Read data from analog Pin 0 from MCP3008 
# Call in loop to get current sensor value
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    if ((adcnum > 7) or (adcnum < 0)):
        return -1

    GPIO.output(cspin, GPIO.HIGH) #True)
    GPIO.output(clockpin, GPIO.LOW) # False)  # Start clock low
    GPIO.output(cspin, GPIO.LOW) # False)     # bring CS low

    commandout = adcnum
    commandout |= 0x18  # Start bit + single-ended bit
    commandout <<= 3    # Only need to send 5 bits here

    for i in range(5):
        if (commandout & 0x80):
            GPIO.output(mosipin, GPIO.HIGH) #True)
        else:
            GPIO.output(mosipin, GPIO.LOW) # False)
        commandout <<= 1
        GPIO.output(clockpin, GPIO.HIGH) # True)
        GPIO.output(clockpin, GPIO.LOW) #False)

    adcout = 0

    # Read in one empty bit, one null bit and 10 ADC bits
    for i in range(12):
        GPIO.output(clockpin, GPIO.HIGH) #True)
        GPIO.output(clockpin, GPIO.LOW) #False)
        adcout <<= 1

        if (GPIO.input(misopin)):
            adcout |= 0x1

    GPIO.output(cspin, GPIO.HIGH) # True)

    adcout /= 2       # first bit is 'null' so drop it

    return adcout
