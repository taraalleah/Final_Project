from machine import Timer
from fifo import Fifo

class Sampler:
    SAMPLE_RATE = 250
    BUFFER_SIZE = 512

    def __init__(self, hardware):
        self.hardware = hardware
        self.fifo = Fifo(self.BUFFER_SIZE, typecode='H')
        self.timer = Timer()

    def timer_callback(self, t):

        try:
            sample = self.hardware.read_sensor()
            self.fifo.put(sample)
        except RuntimeError:
            pass

    def start(self):
        self.timer.init(
            freq=self.SAMPLE_RATE,
            mode=Timer.PERIODIC,
            callback=self.timer_callback
        )

    def stop(self):
        self.timer.deinit()

    def has_sample(self):
        return self.fifo.has_data()

    def get_sample(self):
        return self.fifo.get()