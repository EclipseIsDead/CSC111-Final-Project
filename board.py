import pygame
from constants import BLACK, WHITE, SQUARE_SIZE, ROWS, COLS


class Board:
    def __init__(self):
        self.board = []
        self.selected_piece = None

    def draw_squares(self, window):
        window.fill(WHITE)

        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.rect(window, BLACK, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
