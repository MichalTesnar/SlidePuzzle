# Slide Puzzle
# Originally by Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license
# Slightly modified for the purposes of PYTH01 course at FI MU
# Slightly modified while finishing by me

import pygame
import sys
import random
import copy

# Create the constants (go ahead and experiment with different values)
BOARD_WIDTH = 4  # number of columns in the board
BOARD_HEIGHT = 4  # number of rows in the board
TILE_SIZE = 80
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FPS = 30
BLANK = None
DIFFICULTY = 10

#moje promenne
TURNCOUNTER = 0
GAME_ON = 1
RNDTRNCOUNTER = 50


# Colours are coded as tuples in form of (Red, Green, Blue)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BRIGHT_BLUE = (0, 50, 255)
DARK_TURQUOISE = (3, 54, 73)
GREEN = (0, 204, 0)
RED = (255, 0, 0)

BG_COLOR = DARK_TURQUOISE
TILE_COLOR = GREEN
TEXT_COLOR = WHITE
BORDER_COLOR = BRIGHT_BLUE
BASIC_FONT_SIZE = 20

BUTTON_COLOR = WHITE
BUTTON_TEXT_COLOR = BLACK
MESSAGE_COLOR = WHITE

# margins for tiles
X_MARGIN = int((WINDOW_WIDTH - (TILE_SIZE * BOARD_WIDTH + (BOARD_WIDTH - 1))) / 2)
Y_MARGIN = int((WINDOW_HEIGHT - (TILE_SIZE * BOARD_HEIGHT + (BOARD_HEIGHT - 1))) / 2)

# constants for all four movement directions
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

# global variable to be used in multiple functions, default value is None
FPS_CLOCK = None
DISPLAY_SURFACE = None
BASIC_FONT = None
BUTTONS = None

def get_left_top_of_tile_x(tile_x):
    return(X_MARGIN + tile_x * TILE_SIZE + tile_x - 1)

def get_left_top_of_tile_y(tile_y):
    return(Y_MARGIN + tile_y * TILE_SIZE + tile_y - 1)

def draw_tile(tile_x,tile_y,number,adj_x,adj_y):
    x = get_left_top_of_tile_x(tile_x)
    y = get_left_top_of_tile_y(tile_y)
    tuple1 = (x,y,TILE_SIZE,TILE_SIZE)
    pygame.draw.rect(DISPLAY_SURFACE, TILE_COLOR,tuple1)
    text_surf = BASIC_FONT.render(str(number),True, TEXT_COLOR)
    text_rect = text_surf.get_rect()
    text_rect.center=x+int(TILE_SIZE/2), y+int(TILE_SIZE/2)
    DISPLAY_SURFACE.blit(text_surf,text_rect)

def terminate():
    pygame.quit()
    sys.exit()

def check_for_quit():
    for event in pygame.event.get():
        if (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                terminate()
        elif event.type == pygame.MOUSEBUTTONUP:
            a,b = BUTTONS[0]
            if b.collidepoint(event.pos):
                main()

def get_starting_board():
    plan = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
    cislo=0
    for x in range (0,BOARD_HEIGHT):
        for z in range (0,BOARD_WIDTH):
            cislo+=1
            if cislo==16:
                plan[z][x]="None"
            else:
                plan[z][x]=cislo
    return(plan)

def make_text(text,color,bg_color,top,left):
    text_surf=BASIC_FONT.render(text,True,color,bg_color)
    text_rect=text_surf.get_rect()
    text_rect.topleft = (top,left)
    return(text_surf,text_rect)

def draw_board(board,message):
    global BUTTONS
    DISPLAY_SURFACE.fill(BG_COLOR)
    x,y = make_text(message,WHITE,BG_COLOR,10,10)
    a,b = BUTTONS[0]
    c,d = BUTTONS[1]
    DISPLAY_SURFACE.blit(x,y)
    DISPLAY_SURFACE.blit(a,b)
    DISPLAY_SURFACE.blit(c,d)
    for x in range (0,BOARD_HEIGHT):
        for z in range (0,BOARD_WIDTH):
            if board[x][z]!="None":
                draw_tile(x,z,board[x][z],0,0)

def get_blank_position(board):
    for x in range (0,BOARD_HEIGHT):
        for z in range (0,BOARD_WIDTH):
            if board[x][z]=="None":
                return(x,z)

def make_move(board,move):
    x,z = get_blank_position(board)
    if move=="down":
        board[x][z]=board[x][z-1]
        board[x][z-1]="None"
    elif move=="up":
        board[x][z]=board[x][z+1]
        board[x][z+1]="None"
    elif move=="left":
        board[x][z]=board[x+1][z]
        board[x+1][z]="None"
    elif move=="right":
        board[x][z]=board[x-1][z]
        board[x-1][z]="None"
    

def get_tile_clicked(m,y):
    for x in range (BOARD_WIDTH):
        for z in range (BOARD_HEIGHT):
            a=get_left_top_of_tile_x(x)
            b=get_left_top_of_tile_y(z)
            rect = pygame.Rect(a,b,TILE_SIZE,TILE_SIZE)
            if rect.collidepoint(m,y):
                return(x,z)
    return(None,None)
    

def is_valid_move(board, move):
    x,z=get_blank_position(board)
    if move=="up" and z!=3:
           return(True)
    elif move=="down" and z!=0:
           return(True)
    elif move=="right" and x!=0:
           return(True)
    elif move=="left"and x!=3:
           return(True)
    else:
        return(False)
    
def handle_tile_click(tile_x,tile_y,board):
    blank_x, blank_y = get_blank_position(board)
    if tile_x == blank_x + 1 and tile_y == blank_y:
        return "left"
    elif tile_x == blank_x - 1 and tile_y == blank_y:
        return "right"
    elif tile_x == blank_x and tile_y == blank_y + 1:
        return "up"
    elif tile_x == blank_x and tile_y == blank_y - 1:
        return "down"
    return None

def handle_key_press(key,board):
    if (key == pygame.K_LEFT or key == pygame.K_a) and is_valid_move(board,"left"):
        return("left")
    elif (key == pygame.K_RIGHT or key == pygame.K_d) and is_valid_move(board,"right"):
        return("right")
    elif (key == pygame.K_UP or key == pygame.K_w) and is_valid_move(board,"up"):
        return("up")
    elif (key == pygame.K_DOWN or key == pygame.K_s) and is_valid_move(board,"down"):
        return("down")
    else:
        return("None")

def get_random_move(board,last_move,amount):
    list_of_moves=["left","right","up","down"]
    move=random.choice(list_of_moves)
    if move!=last_move and is_valid_move(board,move) and amount!=0:
        make_move(board, move)
        draw_board(board,"New game")
        get_random_move(board,move,amount-1)
    elif amount!=0:
        get_random_move(board,move,amount)
    else:
        return()

def wait_for_quit(board):
    pygame.draw.rect(DISPLAY_SURFACE,BG_COLOR,(WINDOW_WIDTH-250,WINDOW_HEIGHT-50,80,80))
    message="Vyhráli jste, váš počet tahů je "+str(TURNCOUNTER)
    draw_message(message,165,20,RED,DARK_TURQUOISE)
    pygame.display.update()
    while True:
        check_for_quit()

def draw_message(message,x,y,text_color,bg_color):
    a,b = make_text(message,text_color,bg_color,x,y)
    DISPLAY_SURFACE.blit(a,b)
    

def main():
    global FPS_CLOCK, DISPLAY_SURFACE, BASIC_FONT, BUTTONS
    global RNDTRNCOUNTER, TURNCOUNTER, GAME_ON, BUTTONS
    global solved_board, operational_board, saved_board
    GAME_ON=1    
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Slide Puzzle')
    BASIC_FONT = pygame.font.Font('freesansbold.ttf', BASIC_FONT_SIZE)

    BUTTONS = [
        make_text("New Game",WHITE,DARK_TURQUOISE,WINDOW_WIDTH-150,WINDOW_HEIGHT - 50),
        make_text("Reset",WHITE,DARK_TURQUOISE,WINDOW_WIDTH-250,WINDOW_HEIGHT - 50)]

    solved_board=copy.deepcopy(get_starting_board())
    draw_board(solved_board,"Message")
    operational_board=copy.deepcopy(get_starting_board())
    
    get_random_move(operational_board,"None",RNDTRNCOUNTER)
    saved_board=copy.deepcopy(operational_board)
    
    while GAME_ON==1:
        check_for_quit()
        pygame.display.update()
        FPS_CLOCK.tick(FPS)
        
        for event in pygame.event.get():
            if(event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                terminate()
                
            if event.type == pygame.MOUSEBUTTONUP:
                x,y=get_tile_clicked(event.pos[0],event.pos[1])
                a,b=BUTTONS[0]
                c,d=BUTTONS[1]
                
                if (x,y)!=(None,None):
                    direction = handle_tile_click(x,y,operational_board)
                    make_move(operational_board,direction)
                    TURNCOUNTER+=1
                    draw_board(operational_board,str(TURNCOUNTER))

                    if operational_board==solved_board:
                        GAME_ON=0
                        pygame.display.update()
                        wait_for_quit(operational_board)
                        
                elif b.collidepoint(event.pos[0],event.pos[1]):
                    main()
                elif d.collidepoint(event.pos[0],event.pos[1]):
                    operational_board=copy.deepcopy(saved_board)                    
                    draw_board(operational_board,"Reseted")
                    pygame.display.update()
                
            if event.type == pygame.KEYUP:
                direction = handle_key_press(event.key, operational_board)
                
                if direction!= "None" and is_valid_move(operational_board, direction):
                    make_move(operational_board,direction)
                    TURNCOUNTER+=1
                    draw_board(operational_board,str(TURNCOUNTER))
                    
                    if operational_board==solved_board:
                        GAME_ON=0
                        pygame.display.update()
                        wait_for_quit(operational_board)
        
        

if __name__ == '__main__':
    main()
