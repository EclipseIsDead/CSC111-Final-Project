import pygame
from constants import *


class Board:
    """This is the actual board object."""
    def __init__(self) -> None:
        self.board = STARTING_BOARD
        self.previous_boards = []
        self.selected_piece = None

    def draw_board(self, window) -> None:
        window.fill(pygame.color.Color('white'))

        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.rect(window, pygame.color.Color('black'), (row * SQUARE_SIZE,
                                                 col * SQUARE_SIZE,
                                                 SQUARE_SIZE,
                                                 SQUARE_SIZE), LINE_THICC)

    def draw_pieces(self, window) -> None:
        """We do this later"""

        for col in range(COLS):
            for row in range(ROWS):
                if self.board[col][row] == 'black':
                    rad = SQUARE_SIZE // 2 - LINE_THICC
                    center_pos = (col * SQUARE_SIZE + SQUARE_SIZE / 2, row * SQUARE_SIZE + SQUARE_SIZE / 2)
                    pygame.draw.circle(window, pygame.color.Color('black'), center_pos, rad)
                else:
                    pygame.draw.rect(window, pygame.color.Color(self.board[col][row]), (row * SQUARE_SIZE + LINE_THICC,
                                                     col * SQUARE_SIZE + LINE_THICC,
                                                     SQUARE_SIZE - (2 * LINE_THICC),
                                                     SQUARE_SIZE -(2 * LINE_THICC)), 0)

        self.previous_boards += self.board

    def check_board(self, new_board) -> bool:
        """
        Checks if the next move (therefore the next board state) is not in previous_boards, a list
        containing all previously achieved board states
        """
        if new_board not in self.previous_boards:
            return True
        else:
            return False

    def make_move(self, new_board, window) -> None:
        if self.check_board(new_board):
            self.board = new_board
            self.draw_pieces(window)

