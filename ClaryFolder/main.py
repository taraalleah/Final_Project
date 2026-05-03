from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

import config
import display
import menu

#Oled screen
i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)
display.init(oled)

display.show_start()

#start
menu.run()
