"""This should hold all players."""
import gametree
from typing import Optional
import random


class Player:
    """An abstract class representing an L Game AI.

    This class can be subclassed to implement different strategies for playing chess.
    """

    def make_move(self, game: gametree.GameTree, initial: Optional[list]) -> list:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game
        """
        raise NotImplementedError


class RandomPlayer(Player):
    """An L Game AI whose strategy is always picking a random move."""

    def make_move(self, game: gametree.GameTree, initial: Optional[list]) -> list:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game
        """
        move_set = game.get_valid_moves(initial)
        return random.choice(move_set)


class MiniMaxPlayer(Player):
    """An L Game AI who employs a mini-max strategy."""

    def make_move(self, game: gametree.GameTree, initial: Optional[list]) -> list:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game
        """
        move_set = game.get_valid_moves(initial)
        return random.choice(move_set)


class AlphaBetaPlayer(Player):
    """An L Game AI who employs an alpha-beta pruning strategy."""

    def make_move(self, game: gametree.GameTree, initial: Optional[list]) -> list:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game
        """
        move_set = game.get_valid_moves(initial)
        return random.choice(move_set)


class MCSTPlayer(Player):
    """An L Game AI who employs a Monte Carlo Search Tree strategy."""

    def make_move(self, game: gametree.GameTree, initial: Optional[list]) -> list:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game
        """
        move_set = game.get_valid_moves(initial)
        return random.choice(move_set)
