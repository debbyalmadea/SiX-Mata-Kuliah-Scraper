import json


def read_json(file):
    with open('data/' + file + '.json', 'r') as openfile:
        json_object = json.load(openfile)

        return json_object
