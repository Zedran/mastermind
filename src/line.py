from containers import binds, Geometry
from layout import fonts, layout
import pygame
from resources import settings, theme
from utils import gen_text_object


class Line:
    def __init__(self, display, controller, x, y):
        """
        One line of game code, containing code fields and feedback fields

        :param display: display to which line is to be drawn
        :param x: x coordinate
        :param y: y coordinate
        """
        self.display = display
        self.controller = controller
        self.start_x = x
        self.start_y = y

        self.is_active = False

        self.code = [0 for i in range(settings.code_length)]
        self.feedback = [theme["feedback"]["inactive"] for i in range(settings.code_length)]

        self.bg_field = None
        self.cd_fields = []
        self.fb_fields = []
        self._compute_fields()

        self.line_num_field = Geometry(x=layout.okb.x + layout.okb.w * 0.5,
                                       y=self.start_y + layout.line_h * 0.5,
                                       w=None, h=None)

    def draw_fields(self):
        bg_color = theme["line"]["bg_active"] if self.is_active else theme["line"]["bg_inactive"]
        pygame.draw.rect(self.display, bg_color, self.bg_field)

        self._draw_cd()
        self._draw_fb()

        if not self.is_active:
            self._add_line_number()

    def _draw_cd(self):
        for cd, code_el in zip(self.cd_fields, self.code):
            if not self.is_active and 0 in self.code:
                cd_field_color = theme["field"]["bg_inactive"]
            elif code_el == 0:
                cd_field_color = theme["field"]["bg_empty"]
            else:
                cd_field_color = theme["code"][code_el - 1]

            pygame.draw.rect(self.display, cd_field_color, cd)

            if self.is_active or 0 not in self.code:
                self._add_text(cd_field=cd, code_element=code_el)

            pygame.draw.rect(self.display, theme["field"]["border"], cd, 1)

    def _draw_fb(self):
        for fb, fb_color in zip(self.fb_fields, self.feedback):
            pygame.draw.rect(self.display, fb_color, fb)
            pygame.draw.rect(self.display, theme["field"]["border"], fb, 1)

    def _add_text(self, cd_field, code_element):
        color = theme["text"]["contrast_reversed"] if code_element - 1 in theme["text"]["reversed_for"] else theme["text"]["norm"]

        text_surf, text_rect = gen_text_object(text=str(code_element), font=fonts.code, color=color)
        text_rect.center = (cd_field.x + cd_field.w * 0.5, cd_field.y + cd_field.h * 0.5)
        self.display.blit(text_surf, text_rect)

    def _add_line_number(self):
        text_surf, text_rect = gen_text_object(text=str(self.controller.lines.index(self) + 1),
                                            font=fonts.line_num,
                                            color=theme["line"]["number_text"])
        text_rect.center = (self.line_num_field.x, self.line_num_field.y)
        self.display.blit(text_surf, text_rect)

    def update_code(self, cur_element_idx, button):
        """
        Handles cycling through code chars (range 1 to 8) after clicking
        on one of the code fields of the active line.

        :param cur_element_idx: index of code character corresponding to clicked field
        :param button: which button was pressed over the field?
                       lmb increments, rmb decrements
        """
        i = cur_element_idx
        code_char = self.code[i]

        if button == binds.lmb:
            if code_char >= settings.code_range.max:
                self.code[i] = settings.code_range.min
            else:
                self.code[i] += 1

        elif button == binds.rmb:
            if code_char <= settings.code_range.min:
                self.code[i] = settings.code_range.max
            else:
                self.code[i] -= 1

    def find_collision(self, x, y):
        """
        Checks if specified coordinates collide with code fields.

        :param x: x coordinate of click
        :param y: y coordinate of click

        :returns: if collision is found: index of collided field
                  if field is not active or no collision is found: None
        """
        if not self.is_active:
            return None

        for i, field in enumerate(self.cd_fields):
            if field.collidepoint(x, y):
                return i
        else:
            return None

    def reset(self):
        self.code = [0 for i in range(settings.code_length)]
        self.feedback = [theme["feedback"]["inactive"] for i in range(settings.code_length)]
        self.is_active = False

    def _compute_fields(self):
        """
        Creates rectangles for all fields and the background.
        """
        cd_x = self.start_x + layout.cd_field_spacing
        fb_x = cd_x + settings.code_length * layout.cd_field_size + layout.cd_field_spacing * (settings.code_length + 1)

        self.bg_field = pygame.Rect(
            self.start_x,
            self.start_y,
            layout.line_w,
            layout.line_h
        )

        for i in range(settings.code_length):
            self.cd_fields.append(
                pygame.Rect(
                    cd_x + i * (layout.cd_field_size + layout.cd_field_spacing),
                    self.start_y + 0.5 * (self.bg_field.height - layout.cd_field_size),
                    layout.cd_field_size,
                    layout.cd_field_size
                )
            )

            self.fb_fields.append(
                pygame.Rect(
                    fb_x + i * (layout.fb_field_size + layout.fb_field_spacing),
                    self.start_y + 0.5 * (self.bg_field.height - layout.fb_field_size),
                    layout.fb_field_size,
                    layout.fb_field_size
                )
            )
