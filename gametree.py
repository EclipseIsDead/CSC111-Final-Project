"""
This is the main game tree python file. This stores the tree, game tree and other relevant classes.
"""
from __future__ import annotations
from typing import Optional
from constants import STARTING_BOARD
import numpy as np
from board import Board


class GameTree:
    """A decision tree for L Game moves.

    Each node in the tree stores an L Game board and a boolean representing whether
    the current player (who will make the next move) is Red or Blue. This is based on A2.

    Instance Attributes:
      - move: the current move (expressed in board notation, which is 4x4 of strings)
      - is_red_move: boolean that is True when it is red's move and false if blue's
      - move_type: string that represents what piece is to be moved
      - red_win_probability: the probability that white is going to win the game
    """
    board: Board
    red_win_probability: float

    # Private Instance Attributes:
    #  - _subtrees:
    #      the subtrees of this tree, which represent the game trees after a possible
    #      move by the current player
    _subtrees: list[GameTree]

    def __init__(self, board: Board = Board(), red_win_probability: float = 0.0) -> None:
        """Initialize a new game tree.

        Note that this initializer uses optional arguments, as illustrated below.

        >>> game = GameTree()
        >>> game.move == STARTING_BOARD
        True
        >>> game.is_red_move
        True
        """
        self.board = board
        self._subtrees = []
        self.red_win_probability = red_win_probability

    def get_subtrees(self) -> list[GameTree]:
        """Return the subtrees of this game tree."""
        return self._subtrees

    def find_subtree_by_move(self, move: list) -> Optional[GameTree]:
        """Return the subtree corresponding to the given move.

        Return None if no subtree corresponds to that move.
        """
        for subtree in self._subtrees:
            if subtree.move == move:
                return subtree

        return None

    def add_subtree(self, subtree: GameTree) -> None:
        """Add a subtree to this game tree."""
        self._subtrees.append(subtree)
        for subtree in subtree.get_subtrees():
            subtree._update_red_win_probability()

    def __str__(self) -> str:
        """Return a string representation of this tree.
        """
        return self._str_indented(0)

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_red_move:
            turn_desc = "Red's move"
        else:
            turn_desc = "Blue's move"
        move_desc = f'{self.move} -> {turn_desc}\n'
        s = '  ' * depth + move_desc
        if self._subtrees == []:
            return s
        else:
            for subtree in self._subtrees:
                s += subtree._str_indented(depth + 1)
            return s

    def in_previous_moves(self, curr_move: list) -> bool:
        """Check if the move has been played before."""
        if curr_move in self.board.previous_boards:
            return True
        return False

    def _update_red_win_probability(self) -> None:
        if self.board.is_red_move and len(self.board.get_valid_moves()) == 0:
            self.red_win_probability = -1.0
        elif self.board.is_red_move and len(self.board.get_valid_moves()) != 0:
            self.red_win_probability = 1.0
        else:
            self.red_win_probability = 0.0
