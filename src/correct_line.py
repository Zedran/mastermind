from layout import fonts, layout
import pygame
from resources import settings, theme
from utils import gen_text_object


class CorrectLine:
    def __init__(self, display, x, y, correct_code: list):
        self.display, self.start_x, self.start_y = display, x, y

        self.code = correct_code

        self.bg_field = None
        self.cd_fields = []
        self._compute_fields()

        self.hidden = True

    def draw(self):
        pygame.draw.rect(self.display, theme["line"]["cor_line_bg"], self.bg_field)
        pygame.draw.rect(self.display, theme["field"]["border"], self.bg_field, 1)
        self._draw_hidden() if self.hidden else self._draw_visible()

    def _draw_hidden(self):
        for field in self.cd_fields:
            pygame.draw.rect(self.display, theme["field"]["cor_field_hidden"], field)
            pygame.draw.rect(self.display, theme["field"]["border"], field, 1)

    def _draw_visible(self):
        for char, field in zip(self.code, self.cd_fields):
            pygame.draw.rect(self.display, theme["code"][char - 1], field)
            self._add_text(cd_field=field, code_element=char)
            pygame.draw.rect(self.display, theme["field"]["border"], field, 1)

    def _add_text(self, cd_field, code_element):
        color = theme["text"]["contrast_reversed"] if code_element - 1 in theme["text"]["reversed_for"] else theme["text"]["norm"]

        text_surf, text_rect = gen_text_object(text=str(code_element), font=fonts.code, color=color)
        text_rect.center = (cd_field.x + cd_field.w * 0.5, cd_field.y + cd_field.h * 0.5)
        self.display.blit(text_surf, text_rect)

    def _compute_fields(self):
        cd_x = self.start_x + layout.cd_field_spacing

        self.bg_field = pygame.Rect(
            self.start_x - 1,
            self.start_y,
            settings.code_length * (layout.cd_field_size + layout.cd_field_spacing) + layout.cd_field_spacing,
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
