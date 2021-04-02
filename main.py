import pygame
from constants import WIDTH, HEIGHT
from board import Board


WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('The L Game')

FPS = 30


def main() -> None:
    """
    This is the main function that does BLAH BLAH BLAH
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
                pass

        board.draw_lines(WIN)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
