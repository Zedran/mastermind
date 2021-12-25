from button import Button
from containers import binds, Buttons, signals
from correct_line import CorrectLine
from layout import fonts, layout
from line import Line
import pygame
from resources import lang, settings, theme
from toolbar import Toolbar
from utils import compare_codes, generate_code, gen_text_object, parse_output


class GameBoard:
    def __init__(self, display, x, y, w, h):
        self.display = display

        self.cur_line = 0

        self.bg = pygame.Rect(x, y, w, h)
        self.lines = [Line(display=display, controller=self, x=x, y=y + i * layout.line_h)
                      for i in reversed(range(settings.attempts_num))]

        self.toolbar = Toolbar(display=display, x=0, y=layout.window.h - layout.toolbar_h)

        self.cor_cd_line = CorrectLine(display=display, x=x, y=y - layout.line_h,
                                       correct_code=generate_code(length=settings.code_length, repetitions=False))

        self.ok_button = Button(
            display=self.display,
            x=layout.okb.x,
            y=self.lines[0].bg_field.y + 0.5 * (layout.line_h - layout.okb.h),
            w=layout.okb.w, h=layout.okb.h,
            color_active=theme["buttons"]["ok"]["hover"], color_inactive=theme["buttons"]["ok"]["normal"],
            border_w=1, border_color=theme["buttons"]["ok"]["border"], pressed_down_color=theme["buttons"]["ok"]["pressed"],
            text_color_norm=theme["buttons"]["ok"]["text_norm"], text_color_pressed=theme["buttons"]["ok"]["text_pressed"],
            text=lang["ok"], action=self.submit_code, jump_inc=layout.line_h)

        self.buttons = Buttons(ok=self.ok_button, ng=self.toolbar.ng_button, exit=self.toolbar.ex_button)

        self.game_result = None
        self.game_over_field = pygame.Rect(
            self.cor_cd_line.bg_field.x + self.cor_cd_line.bg_field.w + 1,
            self.cor_cd_line.bg_field.y,
            layout.window.w - 2 * layout.border_size - self.cor_cd_line.bg_field.w + 1,
            layout.line_h)

        self.lines[self.cur_line].is_active = True

    def full_draw(self):
        self.display.fill(theme["window_bg"])

        for line in self.lines:
            line.draw_fields()

        self.cor_cd_line.draw()
        self.toolbar.full_draw()

        if self.game_result is not None:
            self.display_message()

        if self.lines[self.cur_line].is_active:
            self.ok_button.draw()

        pygame.display.update()

    def light_weight_draw(self):
        if self.lines[self.cur_line].is_active:
            self.lines[self.cur_line].draw_fields()
            self.ok_button.draw()

        self.toolbar.light_weight_draw()

        pygame.display.update()

    def display_message(self):
        if self.game_result:
            text_color = theme["end_message"]["won"]["text"]
            bg_color = theme["end_message"]["won"]["bg"]
            text = lang["won"]
        else:
            text_color = theme["end_message"]["lost"]["text"]
            bg_color = theme["end_message"]["lost"]["bg"]
            text = lang["lost"]

        pygame.draw.rect(self.display, bg_color, self.game_over_field)
        pygame.draw.rect(self.display, theme["field"]["border"], self.game_over_field, 1)

        # TODO do something with text displays, this is a mess
        text_surf, text_rect = gen_text_object(text=text, font=fonts.button, color=text_color)
        text_rect.center = (self.game_over_field.x + self.game_over_field.w * 0.5,
                            self.game_over_field.y + self.game_over_field.h * 0.5)
        self.display.blit(text_surf, text_rect)

    def handle_mouse_down(self, x, y, mouse_button_pressed):
        for each in self.buttons:
            if each.find_collision(x, y) and mouse_button_pressed == binds.lmb:
                each.pressed_down = True
                return

        for line in self.lines:
            col = line.find_collision(x, y)
            if col is not None:
                line.update_code(col, mouse_button_pressed)
                break

    def handle_mouse_up(self, x, y, mouse_button_released):
        signal = None
        for each in self.buttons:
            if each.find_collision(x, y) and mouse_button_released == binds.lmb and each.pressed_down:
                signal = each.invoke()
            each.pressed_down = False

        self.full_draw()
        return signal

    def check_mouse_over(self, x, y):
        for each in self.buttons:
            each.mouse_over = True if each.find_collision(x, y) else False

    def submit_code(self):
        if 0 in self.lines[self.cur_line].code:
            return None

        fb = compare_codes(user_code=self.lines[self.cur_line].code,
                           good_code=self.cor_cd_line.code)
        parsed = parse_output(output=fb,
                              hit_objects=(theme["feedback"]["correct"], theme["feedback"]["half_correct"]),
                              empty_object=theme["feedback"]["inactive"],
                              code_length=settings.code_length)

        self.lines[self.cur_line].feedback = parsed

        self._check_for_end_game(parsed_code=parsed)

        return signals.ok

    def _next_line(self):
        self.lines[self.cur_line].is_active = False

        self.cur_line += 1
        if self.cur_line < settings.attempts_num:
            self.lines[self.cur_line].is_active = True
            self.ok_button.jump_up()

    def _lock_current_line(self):
        self.lines[self.cur_line].is_active = False

    def _check_for_end_game(self, parsed_code):
        if parsed_code.count(theme["feedback"]["correct"]) == settings.code_length:
            self._end_game(game_is_won=True)
        elif self.cur_line == settings.attempts_num - 1:
            self._end_game(game_is_won=False)
        else:
            self._next_line()

    def _end_game(self, game_is_won):
        self._lock_current_line()
        self.cor_cd_line.hidden = False
        self.game_result = game_is_won

    def reset(self):
        for line in self.lines:
            line.reset()

        self.game_result = None

        self.ok_button.y += self.cur_line * layout.line_h

        self.cur_line = 0
        self.lines[self.cur_line].is_active = True

        self.cor_cd_line.hidden = True
        self.cor_cd_line.code = generate_code(length=settings.code_length, repetitions=False)
