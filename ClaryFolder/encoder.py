from machine import Pin
import config

rotation = 0     #positive = turned right, negative = turned left
pressed  = False
last_clk = 0     #remembers last encoder clock state

# pins setup
clk = Pin(config.PIN_ENC_CLK, Pin.IN, Pin.PULL_UP)
dt  = Pin(config.PIN_ENC_DT,  Pin.IN, Pin.PULL_UP)
sw  = Pin(config.PIN_ENC_SW,  Pin.IN, Pin.PULL_UP)

last_clk = clk.value()



def on_rotate(pin):
    global rotation, last_clk
    current = clk.value()
    if current == last_clk:
        return                   #ignore noise
    last_clk = current
    if current == 0:             #falling edge = one step happened
        if dt.value() != current:
            rotation += 1       #clockwise = down in menu
        else:
            rotation -= 1       #counter-clockwise = up in menu


def on_press(pin):
    global pressed
    pressed = True


#attach the interrupt handlers to the pins
clk.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=on_rotate)
sw.irq(trigger=Pin.IRQ_FALLING, handler=on_press)



#main f
def get_rotation():
    global rotation
    value = rotation
    rotation = 0
    return value


def was_pressed():
    global pressed
    if pressed:
        pressed = False
        return True
    return False
