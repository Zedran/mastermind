from collections import namedtuple
import json

def load_theme():
    with open(file="user_resources/theme.json", mode="r") as file:
        return json.load(file)


def find_unwanted(line):
    unwanted = '[', ']', '/'
    for char in unwanted:
        if char in line:
            return True
    else:
        return False


def get_file(file: str):
    k_split, v_split, spc, nl = ':', ',', ' ', '\n'

    with open(file=file, mode='r') as settings_file:
        lines = []
        for line in settings_file.readlines():
            if not line.isspace() and not find_unwanted(line):
                splitted = line.split(k_split)
                v = splitted[1].replace(spc, '').replace(nl, '')
                v = v.split(v_split)
                lines.append([splitted[0], v])
    return lines


def load_variables():
    res_idx = "RES"

    parsed = {}
    for line in get_file(file="user_resources/config.txt"):
        k, v = line

        if k == res_idx:
            v = [int(val) for val in v]

        parsed[k] = tuple(v) if len(v) > 1 else v[0]
    return parsed
