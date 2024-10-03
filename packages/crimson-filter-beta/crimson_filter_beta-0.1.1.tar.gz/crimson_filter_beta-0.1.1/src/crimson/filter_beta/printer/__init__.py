import json


def print_json(data, indent=2):
    print(json.dumps(data, indent=indent))
