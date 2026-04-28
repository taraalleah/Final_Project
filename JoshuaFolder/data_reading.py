import json

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
# add_entry({"patient":"A", "hr":80, "bp":120, "timestamp":1})
# add_entry({"patient":"B", "hr":85, "bp":122, "timestamp":2})
# add_entry({"patient":"C", "hr":90, "bp":125, "timestamp":3})
# print(load_data())

#FAKE MQTT TEST

# def send_mqtt(data):
#     print("MQTT")
#     print(data)

