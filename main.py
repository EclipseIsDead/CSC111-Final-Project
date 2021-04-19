"""
CSC111 2021 Final Project - The L Game

This is the main file, which is used to run the L Game and allows for the user to play against an AI

This file is Copyright (c) 2021 Siddarth Dagar, Daniel Zhu, and Bradley Mathi.
"""
from player import *
from gametree import GameTree

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('The L Game')


def main(ai: str) -> None:
    """
    This is the main function that allows for a user to play against an AI of their choice

    Preconditions:
        - ai == '1' or ai == '2'
    """
    board = Board()
    g = GameTree(board)
    p1 = HumanPlayer(g)
    p2 = Player(g)

    if ai == '1':
        p2 = RandomPlayer(g)
    elif ai == '2':
        p2 = MiniMaxPlayer(3, False)
    else:
        print('This is not a valid input')
        exit()

    while len(board.get_valid_moves()) != 0:
        board.draw_board(WIN)
        board.draw_pieces(WIN)
        pygame.display.update()
        # L Piece Red Move
        valid_moves = board.get_valid_moves()
        new_board = p1.make_move(valid_moves, board.board, 'red')
        board.previous_boards.append(board.board)
        board.move_type = 'black'
        board.board = new_board
        board.draw_pieces(WIN)
        pygame.display.update()

        # Neutral Piece Red Move
        yn = input('Would you like to move a neutral piece? "Y" for yes, "N" for no')
        if yn == "Y":
            valid_moves = board.get_valid_moves()
            coords = p1.select_square()
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
        pygame.time.wait(1000)
        board.board = new_board
        board.draw_pieces(WIN)
        pygame.display.update()

        # Neutral Piece Blue Move
        valid_moves = board.get_valid_moves()
        new_board = p2.make_move(board)
        board.previous_boards.append(board.board)
        board.move_type = 'red'
        pygame.time.wait(1000)
        board.board = new_board
        board.draw_pieces(WIN)
        pygame.display.update()

    # Checks and prints winner
    if len(board.get_valid_moves()) == 0:
        winner = board.is_red_move
        if winner == 'red':
            print('Blue has won the game!')
        elif winner == 'blue':
            print('Red has won the game!')


if __name__ == '__main__':
    ai = input('What player would you like to play against? This is an integer from 1 to 4. \n'
               '1) Random Player \n'
               '2) MiniMax Player \n')

    main(ai)
