# Import
import pygame

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# Draw X function
def draw_x(screen, x, y, size, board_type):
    if board_type == 0:
        image = "data/x.png"
    else:
        image = "data/xTransparent.png"
    x_image = pygame.image.load(image).convert_alpha()
    x_image = pygame.transform.scale(x_image, (size, size))
    screen.blit(x_image, [x, y])

    # Pygame graphics
    # pygame.draw.line(screen, BLUE, (x + int(size/8), y), (x + size - int(size/8), y + size), int(size/4))
    # pygame.draw.line(screen, BLUE, (x + int(size/8), y + size), (x + size - int(size/8), y), int(size/4))


# Draw o function
def draw_o(screen, x, y, size, board_type):
    if board_type == 0:
        image = "data/o.png"
    else:
        image = "data/oTransparent.png"
    o_image = pygame.image.load(image).convert_alpha()
    o_image = pygame.transform.scale(o_image, (size, size))
    screen.blit(o_image, [x, y])

    # Pygame graphics
    # pygame.draw.ellipse(screen, RED, [x, y, size, size], int(size/3))
    # pygame.draw.ellipse(screen, RED, [x, y, size, size], int(size / 4))


# Draws board
def draw_board(screen, size, rows, columns, board, board_type):
    # Draws the x's and o's based on the board matrix
    for c in range(columns):
        for r in range(rows):
            if board[r][c] == 1:
                draw_x(screen, c * size, r * size, size, board_type)
            elif board[r][c] == 2:
                draw_o(screen, c * size, r * size, size, board_type)


# Draws grid
def draw_grid(screen, size, rows, columns):
    # Draws the grid based on the columns and rows (Makes 4 thick lines and 12 thin lines in total)
    for c in range(columns):
        for r in range(rows):
            if r != 0 and r % 3 == 0:
                pygame.draw.line(screen, BLACK, (0, r * size), (rows * size, r * size), 3)
            elif r != 0:
                pygame.draw.line(screen, BLACK, (0, r * size), (rows * size, r * size), 1)
        if c != 0 and c % 3 == 0:
            pygame.draw.line(screen, BLACK, (c * size, 0), (c * size, size * rows), 3)
        elif c != 0:
            pygame.draw.line(screen, BLACK, (c * size, 0), (c * size, size * rows), 1)


# Draws the selection rectangle/box highlight
def draw_highlight(screen, size, pos, colour):
    select = pygame.Surface((size, size))
    # Makes square semi transparent
    select.set_alpha(128)
    select.fill(colour)
    screen.blit(select, pos)
