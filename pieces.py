import pygame
from constants import SQUARE_SIZE, BLACK

class HolderPiece:
    """Holder Piece"""
    def __init__(self, row, col):
        self.row = row
        self.col = col

        self.x = 0
        self.y = 0
        self.calculate_position()

    def calculate_position(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def draw_piece(self, window):
        rad = SQUARE_SIZE // 2
        pygame.draw.circle(window, BLACK, (self.x, self.y), rad)

    def move_piece(self, new_row, new_col, window):
        self.row = new_row
        self.col = new_col
        self.calculate_position()
        self.draw_piece(window)

    def check_move(self):
        pass


class PlayerPiece:
    """Player (L) Piece"""
    def __init__(self, position, colour):
        self.position = position
        self.colour = colour

        self.x = 0
        self.y = 0
        self.calculate_position()

    def calculate_position(self):
        """
        Basically, self.position is a list of tuples of the grids (represented by (row, col)) that
        make up an L piece. You loop through each tuple in the list, and then draw in the
        appropriate grids.
        """
        pass

    def draw_piece(self, window):
        pass

    def move_piece(self, new_position, window):
        self.position = new_position
        self.calculate_position()
        self.draw_piece(window)

    def check_move(self):
        pass
