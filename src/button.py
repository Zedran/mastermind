from layout import fonts
import pygame
from utils import gen_text_object


class Button:
    def __init__(self, display, x, y, w, h,
                 color_active, color_inactive, border_w, border_color, pressed_down_color, text_color_norm,
                 text_color_pressed, text='', action=None, jump_inc=0):
        self.display = display

        self.x, self.y = x, y
        self.w, self.h = w, h

        self.color_active = color_active
        self.color_inactive = color_inactive
        self.color_pressed_down = pressed_down_color

        self.border_w = border_w
        self.border_color = border_color

        self.text_color_norm = text_color_norm
        self.text_color_pressed = text_color_pressed

        self.text = text

        self.fg = None
        self.bg = None

        self.action = action
        self.jump_inc = jump_inc

        self.mouse_over = False
        self.pressed_down = False

    def invoke(self):
        if self.mouse_over:
            self.mouse_over = False

        if self.action is not None:
            return self.action()

    def find_collision(self, x, y):
        return self.bg.collidepoint(x, y)

    def draw(self):
        self.bg = pygame.draw.rect(
            self.display, self.border_color,
            (self.x - self.border_w, self.y - self.border_w,
             self.w + self.border_w * 2, self.h + self.border_w * 2)
        )

        if self.pressed_down:
            bg_color = self.color_pressed_down
            text_color = self.text_color_pressed
        elif self.mouse_over:
            bg_color = self.color_active
            text_color = self.text_color_norm
        else:
            bg_color = self.color_inactive
            text_color = self.text_color_norm

        self.fg = pygame.draw.rect(
            self.display, bg_color,
            (self.x, self.y,
             self.w, self.h)
        )

        text_surf, text_rect = gen_text_object(text=self.text, font=fonts.button, color=text_color)
        text_rect.center = (self.x + self.w * 0.5, self.y + self.h * 0.5)
        self.display.blit(text_surf, text_rect)

    def jump_up(self):
        self.y -= self.jump_inc
