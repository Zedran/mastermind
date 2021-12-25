from containers import Range, Settings
import json
import os
import pygame


pygame.font.init()

# ensure the correct working directory for the relative paths to properly point to resources,
# regardless of whether the game is launched through the batch script or directly from source directory
os.chdir(os.path.dirname(os.path.realpath(__file__)))

RES_DIR = "../res"


def load_resource(fname: str) -> dict:
    with open(file=RES_DIR + "/" + fname, encoding="utf-8", mode="r") as file:
        return json.load(file)


config = load_resource("settings/config.json")
lang   = load_resource("settings/langs.json")[config["lang"]]
theme  = load_resource("settings/theme.json")

settings = Settings(
    fps=config["fps"],
    attempts_num=12,
    code_length=4,
    code_range=Range(min=1, max=8),
    repetitions=False  # the game does not handle repetitions for now
)
