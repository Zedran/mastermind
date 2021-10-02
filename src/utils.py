from copy import copy
from random import randint, choice


def gen_text_object(text: str, font, color: tuple):
    """
    Generates text object.

    :param text: string to display
    :param font: pygame font object
    :param color: text color in RGB

    :returns: pygame text object
    """
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def generate_code(length=4, repetitions=False):
    """
    :param length: code length
    :param repetitions: do you want repeating characters in your code?

    :type length: int
    :type repetitions: bool

    :return: generated code
    """
    ext, iterations = (1, 8), range(length)

    code = []
    if repetitions:
        for i in iterations:
            code.append(randint(ext[0], ext[1]))
    else:
        chars = []
        for i in range(ext[0], ext[1] + 1):
            chars.append(i)

        for i in iterations:
            digit = choice(chars)
            chars.remove(digit)
            code.append(digit)

    return code


def compare_codes(user_code, good_code):
    """ Doesn't work for repetitive chars yet

    :param user_code: code specified by a user
    :param good_code: correct code

    :type user_code: list
    :type good_code: list

    :return: tuple (red, white) pins count
    """
    user_code = copy(user_code)
    good_code = copy(good_code)
    red, white = 0, 0
    for i, (uc, gc) in enumerate(zip(user_code, good_code)):
        if uc == gc:
            red += 1
            good_code[i] = 0

    for i, gc in enumerate(good_code):
        if gc in user_code:
            white += 1
            good_code[i] = 0

    return red, white


def parse_output(output, hit_objects, empty_object, code_length):
    red, white = output[0], output[1]
    r_l, wht_l = hit_objects[0], hit_objects[1]

    parsed = []

    for i in range(red):
        parsed.append(r_l)

    for i in range(white):
        parsed.append(wht_l)

    difference = code_length - len(parsed)

    if difference == 0:
        return parsed
    else:
        return parsed + [empty_object for i in range(difference)]
