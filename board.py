import pygame
from constants import *


class Board:
    """This is the actual board object."""
    def __init__(self):
        self.board = [STARTING_BOARD]
        self.selected_piece = None

    def draw_squares(self, window):
        window.fill(WHITE)

        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.rect(window, BLACK, (row * SQUARE_SIZE,
                                                 col * SQUARE_SIZE,
                                                 SQUARE_SIZE,
                                                 SQUARE_SIZE), 1)

    def create_board(self):
        """We do this later"""
        pass
