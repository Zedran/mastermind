from containers import Fonts, Geometry, Layout
import pygame
from resources import config, settings


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

fonts = Fonts(
    code=pygame.font.SysFont("comicsansms", round(0.60606 * layout.toolbar_button_h)),
    button=pygame.font.SysFont("comicsansms", round(0.66667 * layout.toolbar_button_h)),
    line_num=pygame.font.SysFont("comicsansms", round(0.48485 * layout.toolbar_button_h))
)
