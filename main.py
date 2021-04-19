from board import Board
from player import *
from gametree import GameTree

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('The L Game')


def gen_gametree(depth: int, board: Board) -> GameTree:
    """Dub"""
    gametree_so_far = GameTree(board)
    if len(board.get_valid_moves()) == 0:
        if board.is_red_move:
            gametree_so_far.red_win_probability = -1.0
        else:
            gametree_so_far.red_win_probability = 1.0
    elif depth != 0:
        for move in board.get_valid_moves():
            if board.move_type != 'black':
                new_board = Board(move, board.get_valid_moves() + [board.board], board.is_red_move,
                                  'black')
            elif board.is_red_move:
                new_board = Board(move, board.get_valid_moves() + [board.board], False,
                                  'blue')
            else:
                new_board = Board(move, board.get_valid_moves() + [board.board], True,
                                  'red')
            gametree_so_far.add_subtree(gen_gametree(depth - 1, new_board))
    return gametree_so_far



def main(ai: str) -> None:
    """
    This is the main function that does BLAH BLAH BLAH ur mom lol

    Preconditions:
     - ai == '1' or ai == '2' or ai == '3' or ai == '4'
    """
    g = GameTree()
    p1 = HumanPlayer(g)
    p2 = Player(g)
    board = Board()

    if ai == '1':
        p2 = RandomPlayer(g)
    elif ai == '2':
        p2 = MiniMaxPlayer(3, False)
    elif ai == '3':
        p2 = AlphaBetaPlayer(g)
    else:
        print('This is not a valid input')
        exit()

    while len(board.get_valid_moves()) != 0:
        board.draw_board(WIN)
        board.draw_pieces(WIN)
        pygame.display.update()
        # L Piece Red Move
        valid_moves = board.get_valid_moves()
        new_board = p1.make_move(valid_moves, board.board)
        board.previous_boards.append(board.board)
        board.move_type = 'black'
        board.board = new_board
        board.draw_pieces(WIN)
        pygame.display.update()

        # Neutral Piece Red Move
        yn = input('Would you like to move a neutral piece? "Y" for yes, "N" for no')
        if yn == "Y":
            valid_moves = board.get_valid_moves()
            coords = p1.select_square(board.board)
            new_board = p1.move_neutral(valid_moves, board.board, coords)
            board.previous_boards.append(board.board)
            board.board = new_board
            board.draw_pieces(WIN)
            pygame.display.update()
        board.move_type = 'blue'

        # L Piece Blue Move
        valid_moves = board.get_valid_moves()
        new_board = p2.make_move(board)
        board.previous_boards.append(board.board)
        board.move_type = 'black'
        board.board = new_board
        board.draw_pieces(WIN)
        pygame.display.update()

        # Neutral Piece Blue Move
        valid_moves = board.get_valid_moves()
        new_board = p2.make_move(board)
        board.previous_boards.append(board.board)
        board.move_type = 'red'
        board.board = new_board
        board.draw_pieces(WIN)
        pygame.display.update()


if __name__ == '__main__':
    g = GameTree()
    ai = input('What player would you like to play against? This is an integer from 1 to 4. \n'
               '1) Random Player \n'
               '2) MiniMax Player \n'
               '3) AlphaBeta Pruning Player \n')

    main(ai)
