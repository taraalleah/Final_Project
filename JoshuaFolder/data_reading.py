import json

a = open("data.json", "r")
storage = json.load(a)
                   #set json file as list for entry storage

data = {
    "patient" : "Hillary Clinton",
    "hr" : 90,              
    "bp" : 138,
    "timestamp" : 1234556533342424
    }                        #dummy data


storage.append(data)         #append "duh"

b = open("data.json", "w")
json.dump(storage, b)
b.close()                    #dump to json file


print(storage)