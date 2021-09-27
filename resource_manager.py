from collections import namedtuple
import json

RES_DIR = "user_resources"

def load_resource(fname: str) -> dict:
    with open(file=RES_DIR + "/" + fname, encoding="utf-8", mode="r") as file:
        return json.load(file)
