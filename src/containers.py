from collections import namedtuple
import pygame


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
