# reading from ds18x20 to obtain temperature
# then map a temp range to a color range and display
# color with neopixel
# Jon Proctor: added LED(13) Heartbeat
# and adding neopixel support

import time
import board
import simpleio
import neopixel

from adafruit_onewire.bus import OneWireBus
from adafruit_ds18x20 import DS18X20

heartbeat = simpleio.DigitalOut(board.D13)
heartbeat.value = True

# Initialize one-wire bus on board pin D5.
ow_bus = OneWireBus(board.D5)

# Scan for sensors and grab the first one found.
ds18_0 = DS18X20(ow_bus, ow_bus.scan()[0]) # pre  radiator
ds18_1 = DS18X20(ow_bus, ow_bus.scan()[1]) # post radiator
ds18_2 = DS18X20(ow_bus, ow_bus.scan()[2]) # GPU vent
ds18_3 = DS18X20(ow_bus, ow_bus.scan()[3]) # inside temp

# devices = ow_bus.scan()
# for device in devices:
#     print("ROM = {} \tFamily = 0x{:02x}".format([hex(i) for i in device.rom], device.family_code))

# SetUp LED ranges for different displays
LEDArrayLength0 = 14
LEDArrayLength1 = 14
LEDArrayLength2 = 14
LEDArrayLength3 = 14

LEDArray0 = LEDArrayLength0
LEDArray1 = LEDArray0 + LEDArrayLength1
LEDArray2 = LEDArray1 + LEDArrayLength2
LEDArray3 = LEDArray2 + LEDArrayLength3

# SetUp NeoPixels
tempLEDPin = board.A1
numLED = LEDArray0 + LEDArray1+ LEDArray2+ LEDArray3
ORDER = neopixel.GRBW
tempLED = neopixel.NeoPixel(tempLEDPin, numLED, brightness=0.2, auto_write=False, pixel_order=ORDER)

# SetUp temp range and color range.  range for computer: 25 - 65 or 70?
minBTemp = 20
maxBTemp = 30

midGTemp = 32
rngGTemp = 8

minRTemp = 36
maxRTemp = 42


minRed = 0
maxRed = 250
minGrn = 0
maxGrn = 200
minBlu = 250
maxBlu = 0

# Main loop to print the temperature every second.
while True:

    celc_0 = (ds18_0.temperature)
    celc_1 = (ds18_1.temperature)
    celc_2 = (ds18_2.temperature)
    celc_3 = (ds18_3.temperature)

    r_0 = int(((celc_0-minRTemp)/(maxRTemp - minRTemp))*(maxRed-minRed))
    g_0 = int((rngGTemp-(abs(midGTemp - celc_0)))/(rngGTemp) * (maxGrn-minGrn))
    b_0 = int(minBlu-((celc_0-minBTemp)/(maxBTemp - minBTemp))*(minBlu-maxBlu))

    r_1 = int(((celc_1-minRTemp)/(maxRTemp - minRTemp))*(maxRed-minRed))
    g_1 = int((rngGTemp-(abs(midGTemp - celc_1)))/(rngGTemp) * (maxGrn-minGrn))
    b_1 = int(minBlu-((celc_1-minBTemp)/(maxBTemp - minBTemp))*(minBlu-maxBlu))

    r_2 = int(((celc_2-minRTemp)/(maxRTemp - minRTemp))*(maxRed-minRed))
    g_2 = int((rngGTemp-(abs(midGTemp - celc_2)))/(rngGTemp) * (maxGrn-minGrn))
    b_2 = int(minBlu-((celc_2-minBTemp)/(maxBTemp - minBTemp))*(minBlu-maxBlu))

    r_3 = int(((celc_3-minRTemp)/(maxRTemp - minRTemp))*(maxRed-minRed))
    g_3 = int((rngGTemp-(abs(midGTemp - celc_3)))/(rngGTemp) * (maxGrn-minGrn))
    b_3 = int(minBlu-((celc_3-minBTemp)/(maxBTemp - minBTemp))*(minBlu-maxBlu))

    if r_0 < minRed:
        r_0 = minRed
    if g_0 < minGrn:
        g_0 = minGrn
    if b_0 < maxBlu:
        b_0 = maxBlu
    if r_0 > maxRed:
        r_0 = maxRed
    if g_0 > maxGrn:
        g_0 = maxGrn
    if b_0 > minBlu:
        b_0 = minBlu

    if r_1 < minRed:
        r_1 = minRed
    if g_1 < minGrn:
        g_1 = minGrn
    if b_1 < maxBlu:
        b_1 = maxBlu
    if r_1 > maxRed:
        r_1 = maxRed
    if g_1 > maxGrn:
        g_1 = maxGrn
    if b_1 > minBlu:
        b_1 = minBlu

    if r_2 < minRed:
        r_2 = minRed
    if g_2 < minGrn:
        g_2 = minGrn
    if b_2 < maxBlu:
        b_2 = maxBlu
    if r_2 > maxRed:
        r_2 = maxRed
    if g_2 > maxGrn:
        g_2 = maxGrn
    if b_2 > minBlu:
        b_2 = minBlu

    if r_3 < minRed:
        r_3 = minRed
    if g_3 < minGrn:
        g_3 = minGrn
    if b_3 < maxBlu:
        b_3 = maxBlu
    if r_3 > maxRed:
        r_3 = maxRed
    if g_3 > maxGrn:
        g_3 = maxGrn
    if b_3 > minBlu:
        b_3 = minBlu

    # print((celc_0, celc_1, celc_2, celc_3))
    print('pre  radiator:  {0:0.3f}C'.format(celc_0))
    print('post radiator:  {0:0.3f}C'.format(celc_1))
    print('rad C increase: {0:0.3f}C'.format(celc_1 - celc_0))
    print('Inside Temp:    {0:0.3f}C'.format(celc_3))
    print('GPU vent:       {0:0.3f}C'.format(celc_2))
    print('GPU C increase:  {0:0.3f}C'.format(celc_2-celc_3))

    print()

    for i in range(0, LEDArray0, 1):          # Pre radiator
        tempLED[i] = (r_0, g_0, b_0)
    for i in range(LEDArray0, LEDArray1, 1):  # Post Radiator
        tempLED[i] = (r_3, g_3, b_3)
    for i in range(LEDArray1, LEDArray2, 1):  # Inside Temp
        tempLED[i] = (r_1, g_1, b_1)
    for i in range(LEDArray2, LEDArray3, 1):  # GPU Vent
        tempLED[i] = (r_2, g_2, b_2)

    tempLED.show()

# using 'not' for heartbeat to pulse LED(13) for heartbeat
    heartbeat.value = not heartbeat.value

#    time.sleep(0.01)