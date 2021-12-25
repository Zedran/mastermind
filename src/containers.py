from collections import namedtuple
import pygame
from resource_manager import load_resource


pygame.font.init()

Binds    = namedtuple("Binds", 'lmb rmb')
Geometry = namedtuple('Geometry', 'x y w h')
Fonts    = namedtuple('Fonts', 'code button line_num')
Range    = namedtuple("Range", 'min max')
Buttons  = namedtuple("Buttons", "ok ng exit")
Settings = namedtuple("Settings", "fps attempts_num code_length code_range repetitions")
Layout   = namedtuple("Layout", "window border_size line_w line_h lines_spacing cd_field_size cd_field_spacing "
                              "fb_field_size fb_field_spacing cd_to_fb_spacing okb "
                              "toolbar_h toolbar_h_spacing toolbar_button_w toolbar_button_h")


binds   = Binds(lmb=1, rmb=3)
signals = Buttons(ok=None, ng=1, exit=2)

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
