"""
This is the main game tree python file. This stores the tree, game tree and other relevant classes.
"""
from __future__ import annotations
from typing import Optional
from constants import STARTING_BOARD
import numpy as np


class GameTree:
    """A decision tree for L Game moves.

    Each node in the tree stores an L Game board and a boolean representing whether
    the current player (who will make the next move) is Red or Blue. This is based on A2.

    Instance Attributes:
      - move: the current move (expressed in board notation, which is 4x4 of strings)
      - is_red_move: True if Red is to make the next move after this, False otherwise
      - red_win_probability: the probability that white is going to win the game
    """
    move: list
    is_red_move: bool
    red_win_probability: float

    # Private Instance Attributes:
    #  - _subtrees:
    #      the subtrees of this tree, which represent the game trees after a possible
    #      move by the current player
    _subtrees: list[GameTree]

    def __init__(self, move: list = STARTING_BOARD,
                 is_red_move: bool = True, red_win_probability: float = 0.0) -> None:
        """Initialize a new game tree.

        Note that this initializer uses optional arguments, as illustrated below.

        >>> game = GameTree()
        >>> game.move == STARTING_BOARD
        True
        >>> game.is_red_move
        True
        """
        self.move = move
        self.is_red_move = is_red_move
        self._subtrees = []
        self.red_win_probability = red_win_probability

    def get_subtrees(self) -> list[GameTree]:
        """Return the subtrees of this game tree."""
        return self._subtrees

    def find_subtree_by_move(self, move: str) -> Optional[GameTree]:
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
        self._update_red_win_probability()

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

    def is_previous_move(self, curr_move: list) -> bool:
        """Check if the move has been played before."""
        pass

    def get_valid_moves(self, initial: list, red_move: bool) -> list:
        """
        This function returns a list of lists with all possible moves calculated when given a board
        state, and whether it is red's move or not.

        THIS FUNCTION NEEDS TO USE PREVIOUS MOVE FUNCTION AND THEN REMOVE PREVIOUS STATES FROM POSSIBLE.

        Preconditions:
            - initial is represented in move notation

        >>> g = GameTree() # this should load a game tree with only the first position
        >>> len(g.get_valid_moves(STARTING_BOARD, True)) == 5 # this is excluding holder permutations
        """
        move_set = []
        # create a temporary board with a 2 thick border of 'black' to prevent negative indices
        temp = np.pad(np.array(initial), pad_width=2, mode='constant', constant_values='black')

        # there are only 8 permutations of L within each square, treating each square as a corner
        for i in range(len(temp)):
            for j in range(len(temp)):  # iterating through the array temp
                if red_move:
                    viable = {'white', 'red'}
                    colour = 'red'
                    # clear all current reds in the copy of initial board
                    temp = np.where(temp == 'red', 'white', temp)
                else:
                    viable = {'white', 'blue'}
                    colour = 'blue'
                    # clear all current blues in the copy of initial board
                    temp = np.where(temp == 'blue', 'white', temp)

                if temp[i][j] in viable:
                    # if this is a viable spot, or red we can simulate an l piece perm
                    if all(x in viable for x in [temp[i + 1][j], temp[i + 2][j], temp[i][j + 1]]):
                        copy = temp
                        copy[i][j] = copy[i + 1][j] = copy[i + 2][j] = copy[i][j + 1] = colour
                        move_set.append(copy[2:-2, 2:-2])
                    if all(x in viable for x in [temp[i + 1][j], temp[i][j - 1], temp[i][j - 2]]):
                        copy = temp
                        copy[i][j] = copy[i + 1][j] = copy[i][j - 1] = copy[i][j - 2] = colour
                        move_set.append(copy[2:-2, 2:-2])
                    if all(x in viable for x in [temp[i - 1][j], temp[i - 2][j], temp[i][j - 1]]):
                        copy = temp
                        copy[i][j] = copy[i - 1][j] = copy[i - 2][j] = copy[i][j - 1] = colour
                        move_set.append(copy[2:-2, 2:-2])
                    if all(x in viable for x in [temp[i - 1][j], temp[i][j + 1], temp[i][j + 2]]):
                        copy = temp
                        copy[i][j] = copy[i - 1][j] = copy[i][j + 1] = copy[i][j + 2] = colour
                        move_set.append(copy[2:-2, 2:-2])
                    if all(x in viable for x in [temp[i + 1][j], temp[i + 2][j], temp[i][j - 1]]):
                        copy = temp
                        copy[i][j] = copy[i + 1][j] = copy[i + 2][j] = copy[i][j - 1] = colour
                        move_set.append(copy[2:-2, 2:-2])
                    if all(x in viable for x in [temp[i + 1][j], temp[i][j + 1], temp[i][j + 2]]):
                        copy = temp
                        copy[i][j] = copy[i + 1][j] = copy[i][j + 1] = copy[i][j + 2] = colour
                        move_set.append(copy[2:-2, 2:-2])
                    if all(x in viable for x in [temp[i - 1][j], temp[i - 2][j], temp[i][j + 1]]):
                        copy = temp
                        copy[i][j] = copy[i - 1][j] = copy[i - 2][j] = copy[i][j + 1] = colour
                        move_set.append(copy[2:-2, 2:-2])
                    if all(x in viable for x in [temp[i - 1][j], temp[i][j - 1], temp[i][j - 2]]):
                        copy = temp
                        copy[i][j] = copy[i - 1][j] = copy[i][j - 1] = copy[i][j - 2] = colour
                        move_set.append(copy[2:-2, 2:-2])

        # now we scramble the holder pieces in every possible permutation, and add those as well
        for move in move_set:
            pass

        # now check and make sure that no move in the move set has been played before, because
        # repetitions are not valid moves
        for move in move_set:
            if self.is_previous_move(move):
                move_set.remove(move)

        return move_set

    def _update_red_win_probability(self):
        pass
