import pygame
from constants import *
from board import Board
import gametree
import player

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('The L Game')

FPS = 30


def calc_row_col(position: tuple) -> tuple:
    """
    Turns x, y coordinates into row, col
    """
    x, y = position
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE
    return (row, col)


def check_shape(position: tuple, lst: list) -> bool:
    """
    Checks the shape of the inputted move with previous moves
    """
    pass


def main() -> None:
    """
    This is the main function that does BLAH BLAH BLAH ur mom lol
    """
    run = True
    clock = pygame.time.Clock()
    board = Board()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                calc_row_col(position)
                # Need to check the position is L shaped

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
