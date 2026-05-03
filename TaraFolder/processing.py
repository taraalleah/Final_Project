import time

class HeartProcessor:
    THRESHOLD = 32000
    MIN_PEAK_DISTANCE = 75   # ~300ms @250Hz

    def __init__(self, hardware):
        self.hardware = hardware
        
        self.prev_filtered = 0
        self.sample_count = 0
        self.last_peak = 0
        self.bpm = 0

        self.window = []
        self.recent_samples = []

        self.threshold = 32000

    def process(self, sample):

        self.window.append(sample)

        if len(self.window) > 5:
            self.window.pop(0)

        filtered = sum(self.window) // len(self.window)

        self.recent_samples.append(filtered)

        if len(self.recent_samples) > 250:
            self.recent_samples.pop(0)

        if len(self.recent_samples) > 50:
            min_val = min(self.recent_samples)
            max_val = max(self.recent_samples)

            self.threshold = (min_val + max_val) // 2
            
        if (
            filtered > self.threshold and
            self.prev_filtered <= self.threshold
        ):

            if self.sample_count - self.last_peak > self.MIN_PEAK_DISTANCE:

                interval_samples = self.sample_count - self.last_peak
                self.last_peak = self.sample_count

                if interval_samples > 0:
                    ppi = interval_samples / 250
                    bpm = 60 / ppi

                    if 40 <= bpm <= 200:
                        self.bpm = int(bpm)
                        self.hardware.toggle_led()
                        print("Beat detected! BPM:", self.bpm)

        self.prev_filtered = filtered
        self.sample_count += 1

    def get_bpm(self):
        return self.bpm