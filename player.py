"""
CSC111 2021 Final Project - The L Game

This file stores all the player classes and their respective functions. The template for this code
is taken from Assignment 2, specifically the abstract Player class. Credit is given to David Liu,

Liu, David (2021). Assignment 2. CSC111: Trees, Chess, and Artificial Intelligence.
University of Toronto, St. George campus. Synchronous. March 6, 2021.

"""
from gametree import *
from typing import Optional
import random
from constants import *
import pygame


class Player:
    """An abstract class representing an L Game AI.

    This class can be subclassed to implement different strategies for playing chess.
    """
    _game_tree: Optional[GameTree]

    def __init__(self, game_tree: GameTree) -> None:
        """Initialize this player.

        Preconditions:
            - game_tree represents a game tree at the initial state
        """
        self._game_tree = game_tree


class HumanPlayer(Player):
    """The class for the human player"""
    _game_tree: Optional[GameTree]

    def __init__(self, game_tree: GameTree) -> None:
        """Initialize this player.

        Preconditions:
            - game_tree represents a game tree at the initial state
        """
        super().__init__(game_tree)
        self._game_tree = game_tree

    def calc_row_col(self, position: tuple) -> tuple:
        """
        Turns x, y coordinates into (row, col)

        Preconditions:
            - 0 <= position[0] <= ROWS
            - 0 <= position[1] <= COLS
        """
        x, y = position
        col = x // SQUARE_SIZE
        row = y // SQUARE_SIZE
        return (row, col)

    def to_board(self, lst: list[tuple], board: list[list], colour: str) -> list[list]:
        """
        Converts the inputed move into a board

        Preconditions:
            - colour == 'red' or colour == 'blue' or colour == 'black'
            - all({0 <= tuple[0] <= ROWS and 0 <= tuple[0] <= COLS for tuple in lst})
        """
        new_board = board
        for row in range(ROWS):
            for col in range(COLS):
                if board[row][col] == colour:
                    new_board[row][col] = 'white'
                if (row, col) in lst:
                    new_board[row][col] = colour

        return new_board

    def add_piece(self, del_tuple: tuple, add_tuple: tuple, board: list[list]) -> list[list]:
        """
        Moves neutral piece and returns the board after the move

        Preconditions:
            - 0 <= del_tuple[0] <= ROWS
            - 0 <= del_tuple[1] <= COLS
            - 0 <= add_tuple[0] <= ROWS
            - 0 <= add_tuple[1] <= COLS
        """
        new_board = board
        if board[del_tuple[0]][del_tuple[1]] == 'black' and board[add_tuple[0]][
            add_tuple[1]] == 'white':
            new_board[del_tuple[0]][del_tuple[1]] = 'white'
            new_board[add_tuple[0]][add_tuple[1]] = 'black'
        return new_board

    def make_move(self, valid_moves: list[list], board: list[list], colour: str) -> list[list]:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - valid_moves != []
            - colour == 'red' or colour == 'blue'
        """
        run = True
        lst_so_far = new_board = []
        clock = pygame.time.Clock()

        while run:
            clock.tick(FPS)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    new_tuple = self.calc_row_col(position)

                    if new_tuple not in lst_so_far:
                        lst_so_far.append(new_tuple)

                    if len(lst_so_far) == 4:
                        new_board = self.to_board(lst_so_far, board, colour)
                        if new_board in valid_moves:
                            run = False
                        else:
                            print('This is not a valid move.')
                            lst_so_far = new_board = []

        return new_board

    def select_square(self) -> tuple:
        """
        Returns a tuple representing the row and column of the selected square in the pygame window
        """
        run = True
        clock = pygame.time.Clock()
        coords = (0, 0)
        while run:
            clock.tick(FPS)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    coords = self.calc_row_col(position)
                    run = False

        return coords

    def move_neutral(self, valid_moves: list[list], board: list[list], del_coords: [tuple]) -> list[
        list]:
        """
        Returns a new board after moving a neutral piece

        Preconditions:
            - valid_moves != []
            - 0 <= del_coords[0] <= ROWS
            - 0 <= del_coords[1] <= COLS
        """
        run = True
        clock = pygame.time.Clock()
        new_board = board
        while run:
            clock.tick(FPS)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    coords = self.calc_row_col(position)
                    new_board = self.add_piece(del_coords, coords, board)

                    if new_board in valid_moves:
                        run = False
                    else:
                        new_board = board
                        print('This is not a valid move.')

        return new_board


class RandomPlayer(Player):
    """An L Game AI whose strategy is always picking a random move."""
    _game_tree: Optional[GameTree]

    def __init__(self, game_tree: GameTree) -> None:
        """Initialize this player.

        Preconditions:
            - game_tree represents a game tree at the initial state
        """
        super().__init__(game_tree)
        self._game_tree = game_tree

    def make_move(self, initial: Board) -> list[list]:
        """Make a move given the current game by picking a random move of off the current Board"""
        return random.choice(initial.get_valid_moves())


class MiniMaxPlayer(Player):
    """
    An L Game AI who employs a mini-max strategy.
    """
    depth: int
    is_red_player: bool

    def __init__(self, depth: int, is_red_player: bool) -> None:
        """Initialize this player.

        Preconditions:
            - game_tree represents a game tree at the initial state
            - depth >= 0
        """
        self.is_red_player = is_red_player
        self.depth = depth

    def make_move(self, initial: Board) -> list:
        """Make a move given the current game, using a MiniMax algorithim on the generated gametree
        """
        g = gen_gametree(self.depth, initial)

        if g.get_subtrees() == []:
            return initial.board
        else:
            best_move = []
            if initial.is_red_move:
                best_score = -2.0
                for subtree in g.get_subtrees():
                    if subtree.score > best_score:
                        best_score = subtree.score
                        best_move = subtree.board.board
            else:
                best_score = 2.0
                for subtree in g.get_subtrees():
                    if subtree.score < best_score:
                        best_score = subtree.score
                        best_move = subtree.board.board
            return best_move


class _AlphaBetaPlayer(Player):
    """An L Game AI who employs an alpha-beta pruning strategy.

    NOTE: We are not able to implement Alpha Beta Pruning due to the fact that the GameTree's score
    value is already calculated through gen_gametree(). This would have been the part of the code
    that the AB player would have optimized. The code for the AB player to decide it's move is
    present here, as this would be identical to how the MiniMax player would decide."""
    depth: int
    is_red_player: bool

    def __init__(self, depth: int, is_red_player: bool) -> None:
        """Initialize this player.

        Preconditions:
            - game_tree represents a game tree at the initial state
            - depth >= 0
        """
        self.is_red_player = is_red_player
        self.depth = depth

    def make_move(self, initial: Board) -> list:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game
        """
        g = gen_gametree(self.depth, initial)

        if g.get_subtrees() == []:
            return initial.board
        else:
            best_move = []
            if initial.is_red_move:
                best_score = -2.0
                for subtree in g.get_subtrees():
                    if subtree.score > best_score:
                        best_score = subtree.score
                        best_move = subtree.board.board
            else:
                best_score = 2.0
                for subtree in g.get_subtrees():
                    if subtree.score < best_score:
                        best_score = subtree.score
                        best_move = subtree.board.board
            return best_move
