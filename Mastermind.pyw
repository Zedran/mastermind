from containers import lang, layout, settings, signals
from game_board import GameBoard
import os
import pygame
from sys import exit


pygame.init()

os.environ["SDL_VIDEO_CENTERED"] = '1'

game_display = pygame.display.set_mode((layout.window.w, layout.window.h))
pygame.display.set_caption(lang["title"])

try:
    pygame.display.set_icon(pygame.image.load("m.png"))
except pygame.error:
    pass

clock = pygame.time.Clock()
fps   = settings.fps

board = GameBoard(
    display=game_display,
    x=layout.border_size,
    y=layout.border_size + layout.line_h,
    w=layout.line_w,
    h=layout.line_h * settings.attempts_num
)


def shutdown():
    pygame.quit()
    exit(0)


def start_game():
    signal = None

    board.full_draw()
    while signal is None:
        board.light_weight_draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                shutdown()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                board.handle_mouse_down(*event.pos, event.button)
            elif event.type == pygame.MOUSEBUTTONUP:
                signal = board.handle_mouse_up(*event.pos, event.button)

        board.check_mouse_over(*pygame.mouse.get_pos())

        clock.tick(fps)

    return signal


while True:
    next_action = start_game()
    shutdown() if next_action == signals.exit else board.reset()
