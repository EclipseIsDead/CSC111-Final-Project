"""
CSC111 2021 Final Project - The L Game

This is the main gametree file, and thus stores the GameTree class and any appropriate GameTree
functions. Note that the initial tempalte for this code, and the first 5 methods are from
Assignment 2. Credit is given to David Liu,

Liu, David (2021). Assignment 2. CSC111: Trees, Chess, and Artificial Intelligence.
University of Toronto, St. George campus. Synchronous. March 6, 2021.

"""
from __future__ import annotations
from typing import Optional
from constants import STARTING_BOARD
from board import Board


class GameTree:
    """A decision tree for L Game moves.

    Each node in the tree stores an L Game board and a boolean representing whether
    the current player (who will make the next move) is Red or Blue. This is based on A2.

    Instance Attributes:
      - move: the current move (expressed in board notation, which is 4x4 of strings)
      - is_red_move: boolean that is True when it is red's move and false if blue's
      - move_type: string that represents what piece is to be moved
      - score: the probability that white is going to win the game
    """
    board: Board
    score: float

    # Private Instance Attributes:
    #  - _subtrees:
    #      the subtrees of this tree, which represent the game trees after a possible
    #      move by the current player
    _subtrees: list[GameTree]

    def __init__(self, board: Board(), score: float = 0.0) -> None:
        """Initialize a new game tree.

        Note that this initializer uses optional arguments, as illustrated below.

        >>> game = GameTree()
        >>> game.board.board == STARTING_BOARD
        True
        >>> game.board.is_red_move
        True
        """
        self.board = board
        self._subtrees = []
        self.score = score

    def get_subtrees(self) -> list[GameTree]:
        """Return the subtrees of this game tree."""
        return self._subtrees

    def find_subtree_by_move(self, move: list) -> Optional[GameTree]:
        """Return the subtree corresponding to the given move.

        Return None if no subtree corresponds to that move.
        """
        for subtree in self._subtrees:
            if subtree.board.board == move:
                return subtree

        return None

    def add_subtree(self, subtree: GameTree) -> None:
        """Add a subtree to this game tree."""
        self._subtrees.append(subtree)
        for subtree in subtree.get_subtrees():
            subtree._update_score()

    def __str__(self) -> str:
        """Return a string representation of this tree."""
        return self._str_indented(0)

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.board.is_red_move:
            turn_desc = "Red's move"
        else:
            turn_desc = "Blue's move"
        move_desc = f'{self.board.board} -> {turn_desc} \n'
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

    def _update_score(self) -> None:
        """Updates the score of the GameTree based on the score of their subtrees. These scores are
        generated in gen_gametree
        """
        if self.board.is_red_move and self.get_subtrees() != []:
            self.score = max(subtree.score for subtree in self.get_subtrees())
        elif not self.board.is_red_move and self.get_subtrees() != []:
            self.score = min(subtree.score for subtree in self.get_subtrees())
        else:
            return None


def gen_gametree(depth: int, board: Board) -> GameTree:
    """Generates a GameTree and calculates the appropriate score

    Preconditions:
        - depth >= 0
    """
    gametree_so_far = GameTree(board)
    if len(board.get_valid_moves()) == 0:
        if board.is_red_move:
            gametree_so_far.score = -1.0
        else:
            gametree_so_far.score = 1.0
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
