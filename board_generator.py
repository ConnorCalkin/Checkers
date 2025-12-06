import pygame, sys
from pygame.locals import *
from board import GameState, bits_to_indexes, indexes_to_bits, invert
from main import screen_to_index, redraw
WIDTH = 400
HEIGHT = 400

LIGHT_BROWN = (139,69,19)
DARK_BROWN = (255,248,220)
BLACK = (52, 28, 2)
WHITE = (245,222,179)
GOLD = (218,165,32)


coordinates_indexes = {}

start = None
end = None

pygame.init()
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
gamestate = GameState(0,0,0)
redraw(gamestate, DISPLAYSURF)
pygame.display.set_caption('Checkers')
while True: # main game loop
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            index = screen_to_index(pos)
            if index == None:
                continue
            i_bits = indexes_to_bits([index])
            if gamestate.WP & i_bits:
                if gamestate.K & i_bits:
                    gamestate.WP &= invert(i_bits)
                    gamestate.K &= invert(i_bits)
                    gamestate.BP |= i_bits
                else:
                    gamestate.K |= i_bits
            elif gamestate.BP & i_bits:
                if gamestate.K & i_bits:
                    gamestate.WP &= invert(i_bits)
                    gamestate.BP &= invert(i_bits)
                    gamestate.K &= invert(i_bits)
                else:
                    gamestate.K |= i_bits
            else:
                gamestate.WP |= i_bits

            print(f"({gamestate.WP}, {gamestate.BP}, {gamestate.K})")
            redraw(gamestate, DISPLAYSURF)
    pygame.display.update()