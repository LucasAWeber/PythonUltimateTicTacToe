# Ultimate Tic Tac Toe
# May 21, 2021
# ShockingRotom
# Use a matrix to create a playable game of Ultimate Tic Tac Toe

# RULES
# Each turn, you mark one of the small squares
# When you get three in a row on a small board, you’ve won that board.
# To win the game, you need to win three small boards in a row.
# You don’t get to pick which of the nine boards to play on. That’s determined by your opponent’s previous move.
# Whichever square he picks, that’s the board you must play in next. (And whichever square you pick will determine which
# board he plays on next.)

# Importing
import pygame
import math
from data import drawing_library
import numpy as np

pygame.init()

# Colours
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# important variables
COLUMNCOUNT = 9
ROWCOUNT = 9
SQUARESIZE = 50

size = (COLUMNCOUNT * SQUARESIZE, ROWCOUNT * SQUARESIZE)
screen = pygame.display.set_mode(size, 0, 32)

screen.fill(WHITE)
icon = pygame.image.load("data/Icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Ultimate Tic Tac Toe")

clock = pygame.time.Clock()


# Board fill toggle ****************************************************************************************************
board_fill_toggle = False


# Functions ************************************************************************************************************
# Creates a matrix of the board
def create_board(rows, columns):
    board = np.zeros((rows, columns))
    return board


# Checks to make sure the board still have 0 values left
def is_valid(board):
    if 0 in board or 4 in board:
        return True
    else:
        return False


# Function that checks for winning moves
def winning_move(board, piece, rows, columns):
    # check horizontal locations for win
    for c in range(columns - 2):
        for r in range(rows):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece:
                return True

    # check vertical locations for win
    for c in range(columns):
        for r in range(rows - 2):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece:
                return True

    # check positive diagonal
    for c in range(columns - 2):
        for r in range(rows - 2):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece:
                return True

    # check for negative diagonal
    for c in range(columns - 2):
        for r in range(2, rows):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece:
                return True


# Creates the mini boards
def mini_board(board, start_row, start_col):
    return board[start_row * 3:start_row * 3 + 3, start_col * 3:start_col * 3 + 3]


# THIS RULE IS OPTIONAL AND IS CURRENTLY TOGGLED OFF (WITH IT ON ONCE A SMALL BOARD/CELL IS WON NEITHER PLAYER CAN PLAY
# IN IT. WITH IT OFF WHEN A PLAYER WINS A SMALLER BOARD/CELL BOTH PLAYERS CAN STILL PLAY IN IT UNTIL IT IS FILLED
# THE TOGGLE VARIABLE IS LOCATED NEAR THE TOP OF THIS FILE
# Function that fills the mini board with 3s so no x's or os can be placed there and adds the mini board onto THE board
def mini_board_fill(small_board, board, rows, columns, start_row, start_col):
    for c in range(columns):
        for r in range(rows):
            if small_board[r][c] == 0:
                small_board[r][c] = 3
    board[start_row * 3:start_row * 3 + 3, start_col * 3:start_col * 3 + 3] = small_board
    return board


# Loops through 9 times in total creating the mini boards and calling winning_move to check for wins
# This loop is to create and check each section for wins and if there is then add it to the big board
def mini_board_loop(big_board, board):
    # Loops through for each mini board
    for c in range(3):
        for r in range(3):
            # Creates matrix of the current r and c
            mini_board_matrix = mini_board(board, r, c)
            # If the big board has a 0 in the list we just created then check for wins or a tie
            if big_board[r][c] == 0:
                # If player 1 has a winning move then add 1 to the current r and c of the big board
                if winning_move(mini_board_matrix, 1, 3, 3):
                    big_board[r][c] = 1
                    if board_fill_toggle:
                        board = mini_board_fill(mini_board_matrix, board, 3, 3, r, c)
                # If player 2 has a winning move then add 2 to the current r and c of the big board
                elif winning_move(mini_board_matrix, 2, 3, 3):
                    big_board[r][c] = 2
                    if board_fill_toggle:
                        board = mini_board_fill(mini_board_matrix, board, 3, 3, r, c)
                # If neither player won but the space is not valid ei no zeros then make the current r and c of the
                # big board 3 so it will no longer be checked for wins and counts as neither players mini board/ cell
                elif not is_valid(mini_board_matrix):
                    big_board[r][c] = 3
    return board, big_board


# Function that determines the cell you are able to place in
def valid_cell(board, r, c):
    # Subtracts 3 from r and c to find which location the player chose on their mini board to determine the next players
    # Mini board/cell they must play on
    while r >= 3:
        r -= 3
    while c >= 3:
        c -= 3
    # Creates mini board of the next playable cell
    mini_board_matrix = mini_board(board, r, c)
    # If the mini board matrix is valid (has open spots ei has 0s or 4s) then make all 0s in the board 4 and add in the
    # Mini board with zeros back into the board
    if is_valid(mini_board_matrix):
        board = np.where(board == 0, 4, board)
        board[r * 3:r * 3 + 3, c * 3:c * 3 + 3] = mini_board_matrix
    return board


# Places 1 or 2 in the matrix/board
def symbol_place(turn, board, size):
    # Gets the mouse position
    mouse_pos = pygame.mouse.get_pos()
    # Divided the position by the size and rounds down to determine the row and column the player is hovering over
    c = int(math.floor(mouse_pos[0] / size))
    r = int(math.floor(mouse_pos[1] / size))
    # If that value is equal to 0 and not 1 (player 1 symbol), 2 (player 2 symbol), 3 (Toggle-able rule that prevents
    # any player from placing in an already won mini board/cell), and 4 (Used to temporarily cover all the zeros in the
    # Board matrix except the cell the player is playing in)
    if board[r][c] == 0:
        # After verifying that this spot is equal to zero we can make all the temp 4's back to zeros for now
        board = np.where(board == 4, 0, board)
        # Depending on the turn it will place 1 or 2 in that r and c as well as change to next players turn and print
        # The players turn in the console
        if turn == 0:
            board[r][c] = 1
            turn += 1
            print("o's turn")
        else:
            board[r][c] = 2
            turn -= 1
            print("x's turn")
        # Calls the function that controls which cell the next player is able to play in
        board = valid_cell(board, r, c)
    return turn, board


# Mouse highlighting function
def mouse_highlight(screen, size, board):
    # Gets mouse pos
    mouse_pos = pygame.mouse.get_pos()
    # Divides location by the SQUARESIZE and rounds it down to find the column and row the mouse is hovering over
    c = int(math.floor(mouse_pos[0] / size))
    r = int(math.floor(mouse_pos[1] / size))
    # Keeps track of the colour of the main square that follows cursor
    if board[r][c] == 0:
        colour = GREEN
    else:
        colour = RED
    # Multiplies the size back into c and r to get the position of the square on the screen
    pos = (c * size, r * size)
    # Draws the box
    drawing_library.draw_highlight(screen, size, pos, colour)
    # Subtracts 3 from the current row and column until r and c are below 3 to find which location the user is hovering
    # over in the current small board/ cells in order to highlight the small board the next player will play in
    while r >= 3:
        r -= 3
    while c >= 3:
        c -= 3
    # creating the mini board matrix ONLY to verify whether or not the section has any open spot left or not
    # (determining the colour)
    mini_board_matrix = mini_board(board, r, c)
    if not is_valid(mini_board_matrix) and colour != RED:
        colour = ORANGE
    # Makes the square 3 x 3 big in order to fill an entire mini board/ cell
    pos = (c * size * 3, r * size * 3)
    drawing_library.draw_highlight(screen, size * 3, pos, colour)


# Main game loop
def game_loop():

    # Game variables
    turn = 0
    game_over = False

    # Creates the overall board matrix
    board = create_board(ROWCOUNT, COLUMNCOUNT)
    # Creates the big board (the 3 x 3 matrix) that keeps track of the overall winning condition
    big_board = create_board(3, 3)

    # Prints players turn to console
    if turn == 0:
        print("x's turn")
    else:
        print("o's turn")

    while not game_over:
        # User Events ***************************************************
        # Loop waiting for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = True
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                # Calls the symbol place function when player clicks their mouse button
                turn, board = symbol_place(turn, board, SQUARESIZE)

        # Adds to the board and big board every loop
        board, big_board = mini_board_loop(big_board, board)

        # Fills screen
        screen.fill(WHITE)

        # Calling the drawing functions
        drawing_library.draw_board(screen, SQUARESIZE * 3, 3, 3, big_board, 1)
        drawing_library.draw_board(screen, SQUARESIZE, ROWCOUNT, COLUMNCOUNT, board, 0)
        drawing_library.draw_grid(screen, SQUARESIZE, ROWCOUNT, COLUMNCOUNT)
        mouse_highlight(screen, SQUARESIZE, board)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # Checks if anyone won or if the board is filled and saves image of the board if game over
        if winning_move(big_board, 1, 3, 3):
            winner = "Player 1"
            pygame.image.save(screen, "data/UltimateTicTacToeBoard.jpeg")
            return winner
        elif winning_move(big_board, 2, 3, 3):
            winner = "Player 2"
            pygame.image.save(screen, "data/UltimateTicTacToeBoard.jpeg")
            return winner
        elif not is_valid(big_board):
            winner = "Nobody"
            pygame.image.save(screen, "data/UltimateTicTacToeBoard.jpeg")
            return winner


winner = game_loop()
print(str(winner) + " won")
