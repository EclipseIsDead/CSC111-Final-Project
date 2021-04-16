import pygame
from constants import *
from board import Board
from gametree import GameTree
from player import *

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('The L Game')

FPS = 60


def calc_row_col(position: tuple) -> tuple:
    """
    Turns x, y coordinates into row, col
    """
    x, y = position
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    return (row, col)


def to_board(lst: list[tuple], colour: str) -> list[list]:
    """
    Converts the inputed move into a board
    """
    board = STARTING_BOARD
    for col in range(COLS):
        for row in range(ROWS):
            if board[col][row] == colour:
                board[col][row] = 'white'
            if (col, row) in lst:
                board[col][row] = colour

    return board


def main(ai: str, board: Board) -> None:
    """
    This is the main function that does BLAH BLAH BLAH ur mom lol

    Preconditions:
     - ai == '1' or ai == '2' or ai == '3' or ai == '4'
    """
    run = True
    clock = pygame.time.Clock()
    g = GameTree()
    p1 = Player(g, board)
    p2 = Player(g, board)

    if ai == '1':
        p2 = RandomPlayer(g, board)
    elif ai == '2':
        p2 = MiniMaxPlayer(g, board)
    elif ai == '3':
        p2 = AlphaBetaPlayer(g, board)
    elif ai == '4':
        p2 = MCSTPlayer(g, board)
    else:
        print('This is not a valid input')
        run = False

    lst_so_far = []

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                new_tuple = calc_row_col(position)

                if new_tuple not in lst_so_far:
                    lst_so_far.append(new_tuple)

                if len(lst_so_far) == 4:
                    # Basically, if the player inputs 4 moves, we 1) Check the input - if its a
                    # legal move, we follow through and update the board 2) Allow him to move a
                    # black piece 3) Automove for the AI
                    new_board = to_board(lst_so_far, 'red')
                    move_set = g.get_valid_moves(board.board)
                    p1.make_move(new_board, move_set)
                    p2.make_move(new_board, move_set)
                    lst_so_far = []

                print('Pressed')

        board.draw_board(WIN)
        board.draw_pieces(WIN)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    g = GameTree()
    board = Board()
    ai = input('What player would you like to play against? This is an integer from 1 to 4. \n'
               '1) Random Player \n'
               '2) MiniMax Player \n'
               '3) AlphaBeta Pruning Player \n'
               '4) Monte Carlo Search Tree Player \n')

    main(ai, board)
