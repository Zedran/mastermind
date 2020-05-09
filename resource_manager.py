from collections import namedtuple


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


def load_theme():
    FeedbackColors = namedtuple("FeedbackColors", "red white empty")
    ButtonColors = namedtuple("ButtonColors", "normal mouse_over mouse_down border text_norm text_pressed")

    not_color = "CONTRAST REVERSED FOR"

    parsed = {}
    for line in get_file(file="user_resources/theme.txt"):
        k, v = line

        if k == not_color:
            parsed[k] = tuple([int(val) for val in v])
        elif len(v) > 1:
            color_list = []
            for color in v:
                color_list.append(decode_color_hex(color))
            parsed[k] = tuple(color_list)
        else:
            parsed[k] = decode_color_hex(v[0])

    button_indices = "OK", "NEW GAME", "EXIT", "YES", "NO"

    for button in button_indices:
        parsed[button] = ButtonColors(*parsed[button])
    parsed["FEEDBACK"] = FeedbackColors(*parsed["FEEDBACK"])

    return parsed


def load_variables():
    res_idx = "RES"

    parsed = {}
    for line in get_file(file="user_resources/config.txt"):
        k, v = line

        if k == res_idx:
            v = [int(val) for val in v]

        parsed[k] = tuple(v) if len(v) > 1 else v[0]
    return parsed


def decode_color_hex(c_hex: str):
    hex_sig, spc = '#', ' '

    hex_conv_base = 16
    h2_start, h3_start = 2, 4

    c_hex = c_hex.replace(hex_sig, '').replace(spc, '')
    return \
        int(c_hex[:h2_start], hex_conv_base), \
        int(c_hex[h2_start:h3_start], hex_conv_base), \
        int(c_hex[h3_start:], hex_conv_base)
