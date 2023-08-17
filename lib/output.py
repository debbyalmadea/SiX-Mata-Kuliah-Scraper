import json


def save_json(dict, name):
    with open("data/" + name + ".json", "w") as file:
        json.dump(dict, file)
