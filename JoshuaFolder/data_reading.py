import json

data = {
    "patient" : "Dummy",
    "hr" : 40,
    "bp" : 120,
    "timestamp" : 1234556636364353
    }

a = open("data.json", "w")

json.dump(data, a)
a.close()

b = open("data.json", "r")
loaded = json.load(b)
b.close()

print(loaded)