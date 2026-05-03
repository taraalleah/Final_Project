from Project.hardware import Hardware
from Project.sampling import Sampler
from Project.processing import HeartProcessor

hardware = Hardware()
sampler = Sampler(hardware)
processor = HeartProcessor(hardware)

print("Starting heart monitor...")

sampler.start()

while True:
    while sampler.has_sample():
        sample = sampler.get_sample()
        processor.process(sample)

    print("BPM:", processor.get_bpm())