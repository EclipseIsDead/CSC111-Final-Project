"""
This should hold all players.
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
            - game_tree represents a game tree at the initial state (root is '*')
        """
        self._game_tree = game_tree


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
        Turns x, y coordinates into (row, col)
        """
        x, y = position
        col = x // SQUARE_SIZE
        row = y // SQUARE_SIZE
        return (row, col)

    def to_board(self, lst: list[tuple], board: list[list], colour: str) -> list[list]:
        """
        Converts the inputed move into a board
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
        Moves neutral piece and returns the board after
        """
        new_board = board
        if board[del_tuple[0]][del_tuple[1]] == 'black':
            new_board[del_tuple[0]][del_tuple[1]] = 'white'
        if board[add_tuple[0]][add_tuple[1]] == 'white':
            new_board[add_tuple[0]][add_tuple[1]] = 'black'
        return new_board

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
                    pygame.quit()

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
                            lst_so_far = []

        return new_board

    def select_square(self, board: list[list]) -> tuple:
        """
        Selects neutral piece
        """
        run = True
        clock = pygame.time.Clock()
        coords = (0, 0)
        while run:
            clock.tick(FPS)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    coords = self.calc_row_col(position)
                    run = False

        return coords

    def move_neutral(self, valid_moves: list[list], board: list[list], del_coords: [tuple]) -> list[list]:
        """
        Moves neutral piece
        """
        run = True
        clock = pygame.time.Clock()
        new_board = board
        while run:
            clock.tick(FPS)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    position = pygame.mouse.get_pos()
                    coords = self.calc_row_col(position)
                    new_board = self.add_piece(del_coords, coords, board)
                    run = False

                    #if new_board in valid_moves:
                     #   run = False
                    #else:
                     #   print('This is not a valid move.')

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

    def make_move(self, valid_moves: list[list]) -> list[list]:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game
        """
        return random.choice(valid_moves)


class MiniMaxPlayer(Player):
    """
    An L Game AI who employs a mini-max strategy.

    Red is the maximizer, blue is the minimizer.
    """
    _game_tree: Optional[GameTree]
    depth: int

    def __init__(self, game_tree: GameTree, depth: int) -> None:
        """Initialize this player.

        Preconditions:
            - game_tree represents a game tree at the initial state (root is '*')
        """
        super().__init__(game_tree)
        self._game_tree = gen_gametree(depth, Board())
        self.depth = depth

    def make_move(self, valid_moves: list[list]) -> list[list]:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game
        """
        g = self._game_tree
        scores = []
        for move in
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

    def make_move(self, valid_moves: list[list]) -> list[list]:
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
