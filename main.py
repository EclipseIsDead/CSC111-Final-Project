from board import Board
from player import *

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('The L Game')


def main(ai: str) -> None:
    """
    This is the main function that does BLAH BLAH BLAH ur mom lol

    Preconditions:
     - ai == '1' or ai == '2' or ai == '3' or ai == '4'
    """
    g = GameTree()
    p1 = HumanPlayer(g)
    p2 = Player(g)
    board = Board({'red': p1, 'blue': p2})

    if ai == '1':
        p2 = RandomPlayer(g)
    elif ai == '2':
        p2 = MiniMaxPlayer(g)
    elif ai == '3':
        p2 = AlphaBetaPlayer(g)
    else:
        print('This is not a valid input')
        exit()

    while len(board.get_valid_moves()) != 0:
        board.draw_board(WIN)
        board.draw_pieces(WIN)
        pygame.display.update()

        valid_moves = board.get_valid_moves()
        new_board = p1.make_move(valid_moves)
        board.board = new_board
        board.draw_board(WIN)
        board.draw_pieces(WIN)
        pygame.display.update()

        yn = input('Would you like to move a neutral (Black) piece? \n'
                   'Press "Y" for Yes and "N" for No.')
        if yn == 'Y':
            row, col = p1.select_square()[0], p1.select_square()[1]
            if board.board[col][row] == 'black':
                print('True')
                p1.move_neutral((row, col))
            else:
                print('This is not a neutral piece.')


if __name__ == '__main__':
    g = GameTree()
    ai = input('What player would you like to play against? This is an integer from 1 to 4. \n'
               '1) Random Player \n'
               '2) MiniMax Player \n'
               '3) AlphaBeta Pruning Player \n')

    main(ai)
