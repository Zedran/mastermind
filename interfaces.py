from containers import Buttons, binds, fonts, Geometry, lang, layout, settings, signals, theme
from prc import generate_code, compare_codes, parse_output
import pygame


def text_objects(text: str, font, color: tuple):
    """
    Generates text object.

    :param text: string to display
    :param font: pygame font object
    :param color: text color in RGB

    :returns: pygame text object
    """
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


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

        text_surf, text_rect = text_objects(text=str(code_element), font=fonts.code, color=color)
        text_rect.center = (cd_field.x + cd_field.w * 0.5, cd_field.y + cd_field.h * 0.5)
        self.display.blit(text_surf, text_rect)

    def _add_line_number(self):
        text_surf, text_rect = text_objects(text=str(self.controller.lines.index(self) + 1),
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

        text_surf, text_rect = text_objects(text=str(code_element), font=fonts.code, color=color)
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

        text_surf, text_rect = text_objects(text=self.text, font=fonts.button, color=text_color)
        text_rect.center = (self.x + self.w * 0.5, self.y + self.h * 0.5)
        self.display.blit(text_surf, text_rect)

    def jump_up(self):
        self.y -= self.jump_inc


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
                                text=lang.ng, action=self.pass_ng_signal)
        self.ex_button = Button(display, x=button_count * spacing + layout.toolbar_button_w, y=b_y,
                                w=layout.toolbar_button_w, h=layout.toolbar_button_h,
                                color_active=theme["buttons"]["exit"]["hover"], color_inactive=theme["buttons"]["exit"]["normal"],
                                border_w=1, border_color=theme["buttons"]["exit"]["border"],
                                pressed_down_color=theme["buttons"]["exit"]["pressed"],
                                text_color_norm=theme["buttons"]["exit"]["text_norm"], text_color_pressed=theme["buttons"]["exit"]["text_pressed"],
                                text=lang.exit, action=self.pass_exit_signal)

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
            text=lang.ok, action=self.submit_code, jump_inc=layout.line_h)

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
            text = lang.won
        else:
            text_color = theme["end_message"]["lost"]["text"]
            bg_color = theme["end_message"]["lost"]["bg"]
            text = lang.lost

        pygame.draw.rect(self.display, bg_color, self.game_over_field)
        pygame.draw.rect(self.display, theme["field"]["border"], self.game_over_field, 1)

        # TODO do something with text displays, this is a mess
        text_surf, text_rect = text_objects(text=text, font=fonts.button, color=text_color)
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
