import pygame
from constants import BLACK, WHITE, LINE_WIDTH


class Board:
    """This is the actual board object."""
    def __init__(self):
        self.board = []
        self.selected_piece = None

    def draw_lines(self, window):
        window.fill(WHITE)
        pygame.draw.line(window, BLACK, (200, 0), (200, 800), LINE_WIDTH)
        pygame.draw.line(window, BLACK, (400, 0), (400, 800), LINE_WIDTH)
        pygame.draw.line(window, BLACK, (600, 0), (600, 800), LINE_WIDTH)

        pygame.draw.line(window, BLACK, (0, 200), (800, 200), LINE_WIDTH)
        pygame.draw.line(window, BLACK, (0, 400), (800, 400), LINE_WIDTH)
        pygame.draw.line(window, BLACK, (0, 600), (800, 600), LINE_WIDTH)
