import time
import board
import displayio
import terminalio
import adafruit_ahtx0

from adafruit_display_text import label
import adafruit_displayio_sh1107

displayio.release_displays()

# Use for I2C
i2c = board.I2C()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)

# Create the sensor object using I2C
sensor = adafruit_ahtx0.AHTx0(board.I2C())

# SH1107 is vertically oriented 64x128
WIDTH = 128
HEIGHT = 64
BORDER = 2

display = adafruit_displayio_sh1107.SH1107(display_bus, width=WIDTH, height=HEIGHT)

# Make the display context
splash = displayio.Group(max_size=10)
display.show(splash)

# Text set up for Time, Temp, and Humidity
text0 = ("MST:   " )
text1 = ("Temp: %0.1f C" % sensor.temperature)  # overly long to see where it clips
text2 = ("Hum:  %0.1f %%" % sensor.relative_humidity)
text_Time = label.Label(terminalio.FONT, text=text0, color=0xFFFFFF, x=8, y=10)
text_Temp = label.Label(terminalio.FONT, text=text1, color=0xFFFFFF, x=8, y=12)
text_Hum = label.Label(terminalio.FONT, text=text2, color=0xFFFFFF, x=8, y=44)
splash.append(text_Time)
splash.append(text_Temp)
splash.append(text_Hum)

n = 1

while True:
    text_Temp.text = ("\nTemp: %0.1f C" % sensor.temperature)
    text_Temp.x=8
    text_Hum.text = ("Hum:  %0.1f %%" % sensor.relative_humidity)
    text_Hum.x=8
    display.show(splash)
    
    print("\nTemp: %0.1f C" % sensor.temperature)
    print("Hum:  %0.1f %%" % sensor.relative_humidity)
    print(n)
    n=n+1
    time.sleep(1)
