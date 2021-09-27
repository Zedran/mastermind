from collections import namedtuple
import json

def load_config():
    with open(file="user_resources/config.json", mode="r") as file:
        return json.load(file)

def load_theme():
    with open(file="user_resources/theme.json", mode="r") as file:
        return json.load(file)
