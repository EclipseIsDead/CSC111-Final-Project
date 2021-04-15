import pygame
from constants import *
from board import Board

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


def check_shape(position: tuple, lst: list) -> bool:
    """
    Checks the shape of the inputted move with previous moves
    """
    pass


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
    main()
