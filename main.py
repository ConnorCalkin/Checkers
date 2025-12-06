import pygame, sys
from pygame.locals import *
from board import GameState, bits_to_indexes
from ai import AI

WIDTH = 400
HEIGHT = 400

LIGHT_BROWN = (139,69,19)
DARK_BROWN = (255,248,220)
BLACK = (52, 28, 2)
WHITE = (245,222,179)
GOLD = (218,165,32)
HIGHLIGHT = (218,165,32,100)

coordinates_indexes = {}

start = None
end = None

def draw_background(display):
    sq_width = WIDTH / 8
    sq_height = HEIGHT / 8
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 1:
                color = LIGHT_BROWN
            else:
                color = DARK_BROWN
            pygame.draw.rect(display, 
                             color, 
                             (sq_width * i, 
                              sq_height * j,
                              sq_width,
                              sq_height))
        
def draw_checkers(gamestate, display):
    WP = bits_to_indexes(gamestate.WP)
    BP = bits_to_indexes(gamestate.BP)
    K = bits_to_indexes(gamestate.K)
    sq_width = WIDTH / 8
    sq_height = HEIGHT / 8
    padding = 3
    counter = 0
    for j in range(7, -1, -1):
        for i in range(1 - (j % 2), 8, 2):
            coordinates_indexes[(i,j)] = counter
            if counter in WP:
                color = WHITE
            elif counter in BP:
                color = BLACK
            else:
                counter += 1
                continue
            if counter == start:
                pygame.draw.ellipse(display, 
                             HIGHLIGHT, 
                             (sq_width * i, 
                              sq_height * j,
                              sq_width ,
                              sq_height ))
            pygame.draw.ellipse(display, 
                             color, 
                             (sq_width * i + padding, 
                              sq_height * j + padding,
                              sq_width - 2 * padding,
                              sq_height - 2 * padding))
            
            if counter in K:
                pygame.draw.ellipse(display, 
                             GOLD, 
                             (sq_width * i + padding * 4, 
                              sq_height * j + padding * 4,
                              sq_width - 2 * padding * 4,
                              sq_height - 2 * padding * 4))
            
            counter += 1
        
def redraw(gamestate, display):
    draw_background(display)
    draw_checkers(gamestate, display)

def screen_to_index(pos):
    x = pos[0]
    y = pos[1]
    sq_width = WIDTH / 8
    sq_height = HEIGHT / 8
    coord_x = x // sq_width
    coord_y = y // sq_height
    if (coord_x, coord_y) not in coordinates_indexes:
        return None
    else:
        return coordinates_indexes[(coord_x, coord_y)]


def take_turn(display, gamestate, start, end):
    new_state = gamestate.player_move(start, end)
    if new_state:
        gamestate = new_state
        redraw(gamestate, display)
        new_state, _ = ai.minimax(gamestate,8)
        gamestate = new_state
        redraw(gamestate, display)
    return gamestate

if __name__ == "__main__":
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
    gamestate = GameState()
    gamestate.white_turn = True
    ai = AI()
    counter = 0
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
                if start == None:
                    start = index
                    redraw(gamestate, DISPLAYSURF)
                else:
                    end = index
                    new_state = take_turn(DISPLAYSURF, gamestate, start, end)
                    start = None
                    end = None          
                    if new_state:
                        gamestate = new_state
                        redraw(gamestate, DISPLAYSURF)
                    
                    
                
        pygame.display.update()


