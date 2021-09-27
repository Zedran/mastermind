from resource_manager import load_resource
from collections import namedtuple
import pygame


pygame.font.init()

Binds = namedtuple("Binds", 'lmb rmb')
Geometry = namedtuple('Geometry', 'x y w h')
Fonts = namedtuple('Fonts', 'code button line_num')
Range = namedtuple("Range", 'min max')
Buttons = namedtuple("Buttons", "ok ng exit")
Settings = namedtuple("Settings", "fps attempts_num code_length code_range repetitions")
Layout = namedtuple("Layout", "window border_size line_w line_h lines_spacing cd_field_size cd_field_spacing "
                              "fb_field_size fb_field_spacing cd_to_fb_spacing okb "
                              "toolbar_h toolbar_h_spacing toolbar_button_w toolbar_button_h")


signals = Buttons(ok=None, ng=1, exit=2)
binds = Binds(lmb=1, rmb=3)

fonts = Fonts(
    code=pygame.font.SysFont("comicsansms", 20),
    button=pygame.font.SysFont("comicsansms", 22),
    line_num=pygame.font.SysFont("comicsansms", 16)
)

config = load_resource("config.json")
lang   = load_resource("langs.json")[config["lang"]]
theme  = load_resource("theme.json")

settings = Settings(
    fps=30,
    attempts_num=12,
    code_length=4,
    code_range=Range(min=1, max=8),
    repetitions=False
)


res_x, res_y = config["res"]

border_size = 10
line_h = round(res_y * 0.07083)
cd_f_size = round(line_h * 0.6078)
okb_w = cd_f_size * 2
fb_f_end_x = 2 * border_size + 9.625 * cd_f_size
tb_h = res_y - 2 * border_size - line_h * (settings.attempts_num + 1)
tb_h_spacing = 4

layout = Layout(
    window=Geometry(x=None, y=None, w=res_x, h=res_y),
    border_size=border_size,
    line_w=res_x - 2 * border_size,
    line_h=line_h,
    lines_spacing=0,
    cd_field_size=cd_f_size,
    cd_field_spacing=cd_f_size * 0.5,
    fb_field_size=cd_f_size * 0.5,
    fb_field_spacing=cd_f_size * 0.25,
    cd_to_fb_spacing=cd_f_size,
    okb=Geometry(x=fb_f_end_x + 0.5 * (res_x - fb_f_end_x - okb_w - border_size), y=None,
                 w=okb_w, h=cd_f_size * 1.3),
    toolbar_h=tb_h,
    toolbar_h_spacing=tb_h_spacing,
    toolbar_button_w=cd_f_size * 4,
    toolbar_button_h=tb_h - tb_h_spacing

)

del res_x, res_y, border_size, line_h, cd_f_size, okb_w, fb_f_end_x, tb_h, tb_h_spacing
