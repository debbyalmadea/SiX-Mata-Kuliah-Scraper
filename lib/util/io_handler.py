import json


def read_json(file) -> dict:
    with open("data/" + file + ".json", "r") as openfile:
        json_object = json.load(openfile)
        return json_object


def save_json(dict, name) -> None:
    with open("data/" + name + ".json", "w") as file:
        json.dump(dict, file)
