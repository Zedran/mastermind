import json
import os


# ensure the correct working directory for the relative paths to properly point to resources,
# regardless of whether the game is launched through the batch script or directly from source directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))

RES_DIR = "../res"


def load_resource(fname: str) -> dict:
    with open(file=RES_DIR + "/" + fname, encoding="utf-8", mode="r") as file:
        return json.load(file)
