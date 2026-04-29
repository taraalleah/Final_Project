from machine import ADC, Pin

class Hardware:
    def __init__(self):
        self.sensor = ADC(26)
        self.led = Pin(25, Pin.OUT)

    def read_sensor(self):
        return self.sensor.read_u16()

    def toggle_led(self):
        self.led.toggle()