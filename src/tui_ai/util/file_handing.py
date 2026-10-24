import json
def load_json(filename):
    with open(filename,"r") as file:
        data=json.load(file)
    return data
def dump_json(filename,data):
    with open(filename,"w") as file:
        json.dump(data,file,indent=4)
