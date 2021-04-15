"""
This should hold all players.
"""
from gametree import GameTree
from typing import Optional
import random


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

    def make_move(self, g: GameTree) -> None:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game
        """
        raise NotImplementedError


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

    def make_move(self, initial: Optional[list[list]]) -> None:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game
        """
        move_set = self._game_tree.get_valid_moves(initial)
        return random.choice(move_set)


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

    def make_move(self, previous_move: Optional[list[list]]) -> None:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game
        """
        g = self._game_tree
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

    def make_move(self, initial: Optional[list[list]]) -> None:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game
        """
        g = self._game_tree
        minimax = MiniMaxPlayer(g)
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


class MCSTPlayer(Player):
    """An L Game AI who employs a Monte Carlo Search Tree strategy."""
    _game_tree: Optional[GameTree]

    def __init__(self, game_tree: GameTree) -> None:
        """Initialize this player.

        Preconditions:
            - game_tree represents a game tree at the initial state (root is '*')
        """
        super().__init__(game_tree)
        self._game_tree = game_tree

    def make_move(self, initial: Optional[list[list]]) -> None:
        """Make a move given the current game.

        previous_move is the opponent player's most recent move, or None if no moves
        have been made.

        Preconditions:
            - There is at least one valid move for the given game
        """
        raise NotImplementedError
