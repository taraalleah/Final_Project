#Pin number
PIN_SDA     = 4    # OLED screen data pin
PIN_SCL     = 5    # OLED screen clock pin
PIN_PPG     = 26   # Heart rate sensor (ADC)
PIN_LED     = 25   # LED that blinks on each heartbeat
PIN_ENC_CLK = 10   # Encoder rotation pin A
PIN_ENC_DT  = 11   # Encoder rotation pin B
PIN_ENC_SW  = 12   # Encoder push button

#SCreen size
OLED_W = 128
OLED_H = 64

#Sampling
SAMPLE_RATE = 250  

#HR limit (guessing)
BPM_MIN = 40
BPM_MAX = 200

#Menu options
MENU_ITEMS = ["Measure", "History", "Settings"]

#History saved
MAX_HISTORY = 10 #can change
HISTORY_FILE = "history.json" #waiting for jos