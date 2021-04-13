import pygame
from constants import *
from board import Board

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

        grids_so_far = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if len(grids_so_far) == 4:
                pass

            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                # Need to check the position is L shaped
                grids_so_far.append(calc_row_col(position))

        board.draw_board(WIN)
        board.draw_pieces(WIN)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
