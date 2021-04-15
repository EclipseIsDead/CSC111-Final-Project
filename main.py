import pygame
from constants import *
from board import Board
import gametree
import player

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


def main() -> None:
    """
    This is the main function that does BLAH BLAH BLAH ur mom lol
    """
    hold = False
    run = True
    clock = pygame.time.Clock()
    board = Board()
    lst_so_far = []

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                hold = True
                position = pygame.mouse.get_pos()
                calc_row_col(position)
                # Need to check the position is L shaped
                print('Pressed')

            elif event.type == pygame.MOUSEBUTTONUP:
                print('Not Pressed')
                hold = False

            elif event.type == pygame.MOUSEMOTION:
                if hold:
                    position = pygame.mouse.get_pos()
                    new_tuple = calc_row_col(position)

                    if new_tuple not in lst_so_far:
                        lst_so_far.append(new_tuple)

        board.draw_board(WIN)
        board.draw_pieces(WIN)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    g = gametree.GameTree()
    ai = input('What player would you like to play against? This is an integer from 1 to 4. \n'
               '1) Random Player \n'
               '2) MiniMax Player \n'
               '3) AlphaBeta Pruning Player \n'
               '4) Monte Carlo Search Tree Player \n')

    if ai == 1:
        player = player.RandomPlayer(g)
    elif ai == 2:
        player = player.MiniMaxPlayer(g)
    elif ai == 3:
        player = player.AlphaBetaPlayer(g)
    elif ai == 4:
        player = player.MCSTPlayer(g)
    else:
        print('Input not recognized.')

    main()
