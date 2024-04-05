# SPDX-FileCopyrightText: 2021 John Park
# SPDX-License-Identifier: MIT

# I2C rotary encoder multiple test example.
# solder the A0 jumper on the second QT Rotary Encoder board

import board
from adafruit_seesaw import seesaw, rotaryio, digitalio, neopixel
import neopixel as newpixel
import time

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

qt_enc0= seesaw.Seesaw(i2c, addr=0x36) # all open  0 0 0
qt_enc1  = seesaw.Seesaw(i2c, addr=0x37) # A0 closed 1 0 0
qt_enc2= seesaw.Seesaw(i2c, addr=0x38) # A0 closed 0 1 0
qt_enc3= seesaw.Seesaw(i2c, addr=0x39) # A0 closed 1 1 0
qt_enc4= seesaw.Seesaw(i2c, addr=0x3A) # A0 closed 0 1 1
# RTC PCF8523 https://www.adafruit.com/product/5189  0x68

pixel0Bright = 0.2
pixelRed = 0
pixelGrn = 0
pixelBlu = 0

qt_enc0.pin_mode(24, qt_enc0.INPUT_PULLUP)
button0 = digitalio.DigitalIO(qt_enc0, 24)
button0_held = False

qt_enc1.pin_mode(24, qt_enc1.INPUT_PULLUP)
button1 = digitalio.DigitalIO(qt_enc1, 24)
button1_held = False

qt_enc1.pin_mode(24, qt_enc2.INPUT_PULLUP)
button2 = digitalio.DigitalIO(qt_enc2, 24)
button2_held = False

# qt_enc1.pin_mode(24, qt_enc1.INPUT_PULLUP)
# button1 = digitalio.DigitalIO(qt_enc1, 24)
# button_held1 = False

encoder0 = rotaryio.IncrementalEncoder(qt_enc0)
last_position0 = 0

encoder1 = rotaryio.IncrementalEncoder(qt_enc1)
last_position1 = 0

encoder2 = rotaryio.IncrementalEncoder(qt_enc2)
last_position2 = 0

encoder3 = rotaryio.IncrementalEncoder(qt_enc3)
last_position3 = 0

encoder4 = rotaryio.IncrementalEncoder(qt_enc4)
last_position4 = 0

# Set up encoder LED pixels
pixel0 = neopixel.NeoPixel(qt_enc0, 6, 1)
pixel0.brightness = 0.2
pixel0.fill((32, 0, 0))

pixel1 = neopixel.NeoPixel(qt_enc1, 6, 1)
pixel1.brightness = 0.2
pixel1.fill((0, 32, 0))

pixel2 = neopixel.NeoPixel(qt_enc2, 6, 1)
pixel2.brightness = 0.2
pixel2.fill((0, 0, 32))

pixel3 = neopixel.NeoPixel(qt_enc3, 6, 1)
pixel3.brightness = 0.2
pixel3.fill((32, 32, 32))

pixel4 = neopixel.NeoPixel(qt_enc4, 6, 1)
pixel4.brightness = 0.2
pixel4.fill((0, 0, 0))

# SetUp LED array
numLED   = 240
LEDPin = board.D13
ORDER  = neopixel.RGB
LEDStrip = newpixel.NeoPixel(LEDPin, numLED, brightness=1, auto_write=False, pixel_order=ORDER)

# initiate LEDStrip
for i in range(0, len(LEDStrip), 1):
    LEDStrip[i] = (0, 0, 0)

while True:
    position0 = encoder0.position
    position1 = encoder1.position
    position2 = encoder2.position
    position3 = encoder3.position
    position4 = encoder4.position

#Encoder 0
    if position0 != last_position0:  # if they are not equal, the encoder has moved.  the next lines find out which way the enocder moved, and adjust values accordingly
        if position0 > last_position0:
            pixelRed = pixelRed + 8
            print(position0, " ", pixelRed)
        else:
            pixelRed = pixelRed - 8
            print(position0, " ", pixelRed)
            # pixelRed = (pixelRed + 256) % 256  # wrap around to 0-255
        last_position0 = position0

    if not button0.value and not button0_held:
        button_held0 = True
        pixelRed = 0
        print("Button0 pressed", "R= ", pixelRed)

    if button0.value and button0_held:
        button_held0 = False
        # pixelRed = 0
        print("Button 0 released")

# Encoder 1
    if position1 != last_position1:
        if position1 > last_position1:
            pixelGrn = pixelGrn + 8
            print("G = ", position1, " ", pixelGrn)
        else:
            pixelGrn = pixelGrn - 8
            print(position0, " ", pixelGrn)
        last_position1 = position1
    
    if not button1.value and not button1_held:
        button_held1 = True
        pixelGrn = 0
 
    if button1.value and button1_held:
        button_held1 = False
        print("Button 1 released")

# Encoder 2 
    if position2 != last_position2:
        if position2 > last_position2:
            pixelBlu = pixelBlu + 8
            print("B = ", position2, " ", pixelBlu)
        else:
            pixelBlu = pixelBlu - 8
            print(position2, " ", pixelBlu)
        last_position2 = position2
    
    if not button2.value and not button2_held:
        button_held2 = True
        pixelBlu = 0
 
    if button2.value and button2_held:
        button_held2 = False
        print("Button 2 released")

# Encoder 3
    if position3 != last_position3:
        last_position3 = position3
        print("Position 3: {}".format(position3))

# Encoder 4
    if position4 != last_position4:
        last_position4 = position4
        print("Position 4: {}".format(position4))

    for i in range(len(LEDStrip)-1, 0, -1):
        LEDStrip[i] = LEDStrip[i-1]


    LEDStrip[0] = (pixelGrn, pixelRed, pixelBlu)

    LEDStrip.show()

    time.sleep(abs(position4/100))
