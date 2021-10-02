from button import Button
from containers import lang, layout, signals, theme
import pygame


class Toolbar:
    def __init__(self, display, x, y):
        self.display, self.x, self.y = display, x, y
        button_count = 2

        self.bg = pygame.Rect(x, y, layout.window.w, layout.toolbar_h)

        spacing = (self.bg.w - button_count * layout.toolbar_button_w) / (button_count + 1)
        b_x, b_y = x + spacing, y + layout.toolbar_h_spacing * 0.5

        self.ng_button = Button(display, x=b_x, y=b_y,
                                w=layout.toolbar_button_w, h=layout.toolbar_button_h,
                                color_active=theme["buttons"]["ng"]["hover"], color_inactive=theme["buttons"]["ng"]["normal"],
                                border_w=1, border_color=theme["buttons"]["ng"]["border"],
                                pressed_down_color=theme["buttons"]["ng"]["pressed"],
                                text_color_norm=theme["buttons"]["ng"]["text_norm"],
                                text_color_pressed=theme["buttons"]["ng"]["text_pressed"],
                                text=lang["ng"], action=self.pass_ng_signal)
        self.ex_button = Button(display, x=button_count * spacing + layout.toolbar_button_w, y=b_y,
                                w=layout.toolbar_button_w, h=layout.toolbar_button_h,
                                color_active=theme["buttons"]["exit"]["hover"], color_inactive=theme["buttons"]["exit"]["normal"],
                                border_w=1, border_color=theme["buttons"]["exit"]["border"],
                                pressed_down_color=theme["buttons"]["exit"]["pressed"],
                                text_color_norm=theme["buttons"]["exit"]["text_norm"], text_color_pressed=theme["buttons"]["exit"]["text_pressed"],
                                text=lang["exit"], action=self.pass_exit_signal)

    def full_draw(self):
        pygame.draw.rect(self.display, theme["toolbar"], self.bg)
        self.light_weight_draw()

    def light_weight_draw(self):
        self.ng_button.draw()
        self.ex_button.draw()

    @staticmethod
    def pass_ng_signal():
        return signals.ng

    @staticmethod
    def pass_exit_signal():
        return signals.exit
