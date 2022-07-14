import pygame
import random

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
s_width = 800   # screen width
s_height = 700  # screen height
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 30 height per block
block_size = 30

# starting x and y positions
top_left_x = (s_width - play_width) // 2    # actual play area. To see the closure sort of things
top_left_y = s_height - play_height

# SHAPE FORMATS

S = [['.....',  # 5x5 grid. '00' represents where the blocks actually is.
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


# index 0 - 6 represent shape


class Piece(object):    # main info holder for all
    rows = 20  # y
    columns = 10  # x

    def __init__(self, column, row, shape):     # constructor created to create an object of the class later on
        self.x = column                         # and to allow the class to initialize the attributes of the class
        self.y = row
        self.shape = shape
        # # as the colour for a shape is the same index as the index of the shape in the shapes list
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0  # number from 0-3


def create_grid(locked_positions={}):

    # 2D list in which contains list of 10 colors
    # one list for every row in our grid
    # ie, for every 20 rows in the grid we have 20 sub-lists for eah row
    # each sublist contains 10 colours because we have 10 squares in each row and we have 20 rows total
    # (0,0,0)= black colour grid

    grid = [[(0, 0, 0) for x in range(10)] for x in range(20)]

    # for the blocks in the grid which are already occupied by shapes
    # so we need to find those positions and replace them with colours so get we get
    # the locked_positions filled with colours of the shapes

    for i in range(len(grid)):  # enter in the main list
        for j in range(len(grid[i])):   # enter in the sublist
            if (j, i) in locked_positions:
                c = locked_positions[(j, i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)    # we are making a list of all the shapes coming from format
        for j, column in enumerate(row):
            if column == '0':
                # if 0 exists in the col, add the position to the list
                positions.append((shape.x + j, shape.y + i))
                # adding the current value of x to j=col value
                # lly, adding the current value of y to i=row value
    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)     # deleting the extra spaces, ie, offsetting it

    return positions


def valid_space(shape, grid):
    # creating 2D list same as create_grid
    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    # convert it into 1D. Taking all the positions from the above 2D and adding it into the 1d list
    accepted_positions = [j for sub in accepted_positions for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False

    return True


def check_lost(positions):
    for pos in positions:   # check if position is outside the grid
        x, y = pos
        if y < 1:           # if position of y>1. We loss the game
            return True
    return False


def get_shape():            # to let random shapes come into the grid when the game starts
    global shapes, shape_colors

    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(text, size, color, surface):
    font = pygame.font.SysFont('comic sans', size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2),
                         top_left_y + play_height / 2 - label.get_height() / 2))


def draw_grid(surface, row, col):
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * 30), (sx + play_width, sy + i * 30))
        # horizontal lines. y values will remain same. Only x values changes, from up to down
        for j in range(col):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * 30, sy), (sx + j * 30, sy + play_height))
            # vertical lines. x values will remain same. Only y values changes, left to right


def clear_rows(grid, locked):
    # need to see if row is clear the shift every other row above down one

    inc = 0
    for i in range(len(grid) - 1, -1, -1):  # loop through grid backwards so that we don't overlap on shapes
        row = grid[i]
        if (0, 0, 0) not in row:    # this means there is no black space in the grid, all coloured/filled with shapes
            inc += 1
            # add positions to remove from locked
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]  # the locked position/ filled needs to be removed by this code
                except:
                    continue

    # now to shift the remaining, ie move. To do this, when we remove a del a row at bottom, we need to add a new row
    # up of the grid to maintain the dimensions
    if inc > 0:     # ie, we removed at least on row
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key

            # if the current y position to be deleted is below the current index position
            # then move all above y, one step down
            if y < ind:
                newKey = (x, y + inc)   # inc tells us how many rows got deleted, so we need to move down that many rows
                locked[newKey] = locked.pop(key)


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comic sans', 30)
    label = font.render('Next Shape', 1, (255, 255, 255))

    # for the drawing that comes in the side of the window
    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height / 2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j * 30, sy + i * 30, 30, 30), 0)

    surface.blit(label, (sx + 10, sy - 30))


def draw_window(surface):
    surface.fill((0, 0, 0))

    # Tetris Title
    pygame.font.init()
    font = pygame.font.SysFont('comic sans', 60)
    label = font.render('TETRIS', 1, (255, 255, 255))  # set it to white

    # now draw the label on the screen (on center/ middle of the screen)
    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * 30, top_left_y + i * 30, 30, 30), 0)

    # draw the red border
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

    draw_grid(surface, 20, 10)


def main():
    global grid

    locked_positions = {}  # (x,y):(255,0,0)
    grid = create_grid(locked_positions)

    # while loop
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    level_time = 0
    fall_speed = 0.27
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()        # raw time gives the amt of time since the clock.tick()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time / 1000 > 4:
            level_time = 0
            if fall_speed > 0.15:
                fall_speed -= 0.005

        # PIECE FALLING CODE
        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # to quit
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:    # to throw down the shapes

                if event.key == pygame.K_LEFT:  # to move piece left
                    current_piece.x -= 1    # move left
                    if not valid_space(current_piece, grid):    # if no space towards left
                        current_piece.x += 1     # move to current pos and oretend to not move at all

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1

                elif event.key == pygame.K_UP:
                    # rotate shape
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

                if event.key == pygame.K_DOWN:
                    # move shape down
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

        # check the pos of the pieces and decide whether to we need walk more or we have reached the ground
        shape_pos = convert_shape_format(current_piece)

        # add piece to the grid for drawing, ie, occupy the grid pos with the piece
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        # IF PIECE HIT GROUND
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
                # a dict that contains a tuple of the position : value of color
                # so we get the info if piece reached ground and hence we can update the color of the grid accordingly

            current_piece = next_piece      # if reached ground, next piece will be a new piece now
            next_piece = get_shape()
            change_piece = False

            # call four times to check for multiple clear rows
            if clear_rows(grid, locked_positions):
                score += 10

        draw_window(win)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        # Check if user lost
        if check_lost(locked_positions):
            run = False

    draw_text_middle("You Lost", 40, (255, 255, 255), win)
    pygame.display.update()
    pygame.time.delay(2000)


def main_menu():
    run = True
    while run:
        win.fill((0, 0, 0))
        draw_text_middle('Press any key to begin.', 60, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')

main_menu()  # start game

