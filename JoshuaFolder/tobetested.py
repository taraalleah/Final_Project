import json
import network
from time import sleep
from umqtt.simple import MQTTClient

SSID = "KME_751_G1"
PASSWORD = "korvapuusti"
BROKER_IP = "192.168.1.69"
PORT = 21883

def connect_wlan():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    while wlan.isconnected() == False:
        print("Connecting...")
        sleep(1)

    print("Connection successful. Pico IP:", wlan.ifconfig()[0])

def connect_mqtt():
    global mqtt_client
    mqtt_client = MQTTClient("pico", server=BROKER_IP, port=PORT)
    mqtt_client.connect(clean_session=True)
    return mqtt_client

def load_data():
    i = open("data.json", "r")
    data = json.load(i)
    i.close()
    return data

def save_data(data):
    i = open("data.json", "w")
    json.dump(data, i)
    i.close()

def add_entry(entry):
    data = load_data()
    data.append(entry)
    save_data(data)
    send_mqtt(entry)
    
def send_mqtt(data):
    topic = "jostacla"
    message = json.dumps(data)
    mqtt_client.publish(topic, message)
    print("MQTT")
    print(message)

connect_wlan()
connect_mqtt()

add_entry({
    "patient": "test",
    "hr": 80,
    "bp": 120,
    "timestamp": 1
    })
