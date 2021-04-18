"""
This should hold all players.
"""
from gametree import GameTree
from typing import Optional
import random
from constants import *
import pygame


class Player:
    """An abstract class representing an L Game AI.

    This class can be subclassed to implement different strategies for playing the L Game.
    """
    _game_tree: Optional[GameTree]

    def __init__(self, game_tree: GameTree) -> None:
        """Initialize this player.

        Preconditions:
            - game_tree represents a game tree at the initial state (root is '*')
        """
        self._game_tree = game_tree

    def make_move(self, valid_moves: list[list], board: list[list]) -> list[list]:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game
        """
        raise NotImplementedError


class HumanPlayer(Player):
    """An L Game AI whose strategy is always picking a random move."""
    _game_tree: Optional[GameTree]

    def __init__(self, game_tree: GameTree) -> None:
        """Initialize this player.

        Preconditions:
            - game_tree represents a game tree at the initial state (root is '*')
        """
        super().__init__(game_tree)
        self._game_tree = game_tree

    def calc_row_col(self, position: tuple) -> tuple:
        """
        Turns x, y coordinates into row, col
        """
        x, y = position
        col = x // SQUARE_SIZE
        row = y // SQUARE_SIZE
        return (row, col)

    def to_board(self, lst: list[tuple], board: list[list], colour: str) -> list[list]:
        """
        Converts the inputed move into a board
        """
        board = board
        for col in range(COLS):
            for row in range(ROWS):
                if board[col][row] == colour:
                    board[col][row] = 'white'
                if (col, row) in lst:
                    board[col][row] = colour

        return board

    def del_piece(self, tuple: tuple, board: list[list]) -> list[list]:
        """
        Deletes a piece and returns the board after
        """
        board = board
        for col in range(COLS):
            for row in range(ROWS):
                if board[col][row] == 'black' and row == tuple[0] and col == tuple[1]:
                    board[col][row] = 'white'
        return board

    def add_piece(self, tuple: tuple, board: list[list]) -> list[list]:
        """
        Deletes a piece and returns the board after
        """
        board = board
        for col in range(COLS):
            for row in range(ROWS):
                if board[col][row] == 'white' and row == tuple[0] and col == tuple[1]:
                    board[col][row] = 'black'
        return board

    def make_move(self, valid_moves: list[list], board: list[list]) -> list[list]:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game
        """
        run = True
        lst_so_far = new_board = []
        clock = pygame.time.Clock()

        while run:
            clock.tick(FPS)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    run = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    new_tuple = self.calc_row_col(position)

                    if new_tuple not in lst_so_far:
                        lst_so_far.append(new_tuple)

                    if len(lst_so_far) == 4:
                        new_board = self.to_board(lst_so_far, board, 'red')
                        if new_board in valid_moves:
                            board = new_board
                            run = False
                        else:
                            print('This is not a valid move.')

        return new_board

    def select_square(self, board: list[list]) -> list[list]:
        """
        Select neutral piece
        """
        run = True
        clock = pygame.time.Clock()
        coords = (0, 0)
        while run:
            clock.tick(FPS)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    run = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    coords = (self.calc_row_col(position)[0], self.calc_row_col(position)[1])
                    run = False

        return self.del_piece(coords, board)

    def move_neutral(self, valid_moves: list[list], board: list[list]) -> list[list]:
        """
        Move neutral piece
        """
        run = True
        clock = pygame.time.Clock()
        new_board = []
        while run:
            clock.tick(FPS)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    run = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    coords = (self.calc_row_col(position)[0], self.calc_row_col(position)[1])

                    if self.add_piece(coords, board) in valid_moves:
                        new_board = self.add_piece(coords, board)
                        run = False
                    else:
                        print('This is not a valid move.')

        return new_board


class RandomPlayer(Player):
    """An L Game AI whose strategy is always picking a random move."""
    _game_tree: Optional[GameTree]

    def __init__(self, game_tree: GameTree) -> None:
        """Initialize this player.

        Preconditions:
            - game_tree represents a game tree at the initial state (root is '*')
        """
        super().__init__(game_tree)
        self._game_tree = game_tree

    def make_move(self, valid_moves: list[list], board: list[list]) -> list[list]:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game
        """
        return random.choice(valid_moves)


class MiniMaxPlayer(Player):
    """An L Game AI who employs a mini-max strategy."""
    _game_tree: Optional[GameTree]

    def __init__(self, game_tree: GameTree) -> None:
        """Initialize this player.

        Preconditions:
            - game_tree represents a game tree at the initial state (root is '*')
        """
        super().__init__(game_tree)
        self._game_tree = game_tree

    def make_move(self, valid_moves: list[list], board: list[list]) -> list[list]:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game
        """
        g = self._game_tree
        pass
        """
        if leaf(n) then return evaluate(n)
        if n is a max node
            v := L
            for each child of n
                v' := minimax (child)
                if v' > v, v:= v'
            return v
        if n is a min node
            v := W
            for each child of n
                v' := minimax (child)
                if v' < v, v:= v'
            return v     
        """
        raise NotImplementedError


class AlphaBetaPlayer(Player):
    """An L Game AI who employs an alpha-beta pruning strategy."""
    _game_tree: Optional[GameTree]

    def __init__(self, game_tree: GameTree) -> None:
        """Initialize this player.

        Preconditions:
            - game_tree represents a game tree at the initial state (root is '*')
        """
        super().__init__(game_tree)
        self._game_tree = game_tree

    def make_move(self, valid_moves: list[list], board: list[list]) -> list[list]:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game
        """
        minimax = MiniMaxPlayer(self._game_tree)
        pass
        """
        if leaf(n) or depth=0 return evaluate(n)
        if n is a max node
            v := min
            for each child of n
                v' := minimax (child,d-1,...,...)
                if v' > v, v:= v'
                if v > max return max
            return v
        if n is a min node
            v := max
            for each child of n
                v' := minimax (child,d-1,...,...)
                if v' < v, v:= v'
                if v < min return min
            return v
        """
        raise NotImplementedError
