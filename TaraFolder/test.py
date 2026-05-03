from machine import ADC
import time

adc = ADC(26)

prev_raw = 0
last_value = 0

threshold = 30000   # adjust this
sample = 0
last_peak_sample = 0
beats = 0
start_time = time.ticks_ms()

while True:

    raw = adc.read_u16()
    value = (raw + prev_raw) // 2
    prev_raw = raw

    if last_value > value and last_value > threshold:

        if sample - last_peak_sample > 150:
            beats += 1
            last_peak_sample = sample
            print("❤Bubump!") #reading

    last_value = value

    elapsed = time.ticks_diff(time.ticks_ms(), start_time)

    if elapsed >= 10000:
        bpm = beats * 6
        print("BPM:", bpm)
        beats = 0
        start_time = time.ticks_ms()

    sample += 1

    time.sleep(1/250)