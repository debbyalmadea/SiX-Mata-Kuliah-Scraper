import json


def read_json(file) -> dict:
    try:
        with open("data/" + file + ".json", "r") as openfile:
            json_object = json.load(openfile)
            return json_object
    except FileNotFoundError:
        return None


def save_json(data_dict, name) -> None:
    with open("data/" + name + ".json", "w") as file:
        json.dump(data_dict, file)
