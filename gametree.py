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
      - is_red_move: boolean that is True when it is red's move and false if blue's
      - move_type: string that represents what piece is to be moved
      - red_win_probability: the probability that white is going to win the game
    """
    move: list
    is_red_move: bool
    move_type: str
    red_win_probability: float

    # Private Instance Attributes:
    #  - _subtrees:
    #      the subtrees of this tree, which represent the game trees after a possible
    #      move by the current player
    _subtrees: list[GameTree]

    def __init__(self, move: list = STARTING_BOARD, is_red_move: bool = True,
                 move_type: str = 'red', red_win_probability: float = 0.0) -> None:
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
        self.move_type = move_type
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

    def in_previous_moves(self, curr_move: list) -> bool:
        """Check if the move has been played before."""
        if curr_move in self.get_subtrees():
            return False
        return True

    def get_valid_moves(self, initial: list[list]) -> list:
        """
        This function returns a list of lists with all possible moves calculated when given a board
        state, and whether it is red's move or not. THIS FUNCTION NEEDS TO USE PREVIOUS MOVE
        FUNCTION AND THEN REMOVE PREVIOUS STATES FROM POSSIBLE.

        Preconditions:
            - initial is represented in move notation

        >>> g = GameTree() # this should load a game tree with only the first position
        >>> len(g.get_valid_moves(STARTING_BOARD)) == 5
        True
        """
        move_set = []
        if self.move_type == 'black':
            # do the neutral piece shuffle
            # now we scramble the holder pieces in every possible permutation, and add those as well
            temp = np.array(initial)
            # 2 arrays where the top and bottom neutral pieces are removed respectively
            top_and_bottom = [temp.copy(), temp.copy()]

            # remove the top piece from top
            for i in range(len(temp)):
                for j in range(len(temp)):
                    if temp[i][j] == 'black':
                        top_and_bottom[0][i][j] = 'white'
                        break

            # remove the bottom piece from bottom
            for i in range(len(temp)):
                for j in range(len(temp)):
                    if top_and_bottom[0][i][j] == 'black':
                        top_and_bottom[1][i][j] = 'white'
                        break

            # adds all possible neutral piece configs to move_set (with an extra initial state)
            for array in top_and_bottom:
                for i in range(len(temp)):
                    for j in range(len(temp)):
                        if array[i][j] == 'white':
                            copy = array.copy()
                            copy[i][j] = 'black'
                            move_set.append(copy.tolist())
            # end of if branch
        else:
            # create a temporary board with a 2 thick border of 'black' to prevent negative indices
            temp = np.pad(np.array(initial), pad_width=2, mode='constant', constant_values='gray')

            # begin by removing the l-piece in question
            for i in range(2, len(temp) - 2):
                for j in range(2, len(temp) - 2):
                    if temp[i][j] == self.move_type:
                        temp[i][j] = 'white'

            # there are only 8 permutations of L within each square, treating each square as corner
            for i in range(2, len(temp) - 2):
                for j in range(2, len(temp) - 2):  # iterating through the array temp
                    if temp[i][j] == 'white':
                        # if this is a viable spot, or red we can simulate an l piece perm
                        if all(x == 'white' for x in
                               [temp[i + 1][j], temp[i + 2][j], temp[i][j + 1]]):
                            copy = np.copy(temp)
                            copy[i][j] = copy[i + 1][j] \
                                = copy[i + 2][j] = copy[i][j + 1] = self.move_type
                            move_set.append(copy[2:-2, 2:-2].tolist())
                        if all(x == 'white' for x in
                               [temp[i + 1][j], temp[i][j - 1], temp[i][j - 2]]):
                            copy = np.copy(temp)
                            copy[i][j] = copy[i + 1][j] \
                                = copy[i][j - 1] = copy[i][j - 2] = self.move_type
                            move_set.append(copy[2:-2, 2:-2].tolist())
                        if all(x == 'white' for x in
                               [temp[i - 1][j], temp[i - 2][j], temp[i][j - 1]]):
                            copy = np.copy(temp)
                            copy[i][j] = copy[i - 1][j] \
                                = copy[i - 2][j] = copy[i][j - 1] = self.move_type
                            move_set.append(copy[2:-2, 2:-2].tolist())
                        if all(x == 'white' for x in
                               [temp[i - 1][j], temp[i][j + 1], temp[i][j + 2]]):
                            copy = np.copy(temp)
                            copy[i][j] = copy[i - 1][j] \
                                = copy[i][j + 1] = copy[i][j + 2] = self.move_type
                            move_set.append(copy[2:-2, 2:-2].tolist())
                        if all(x == 'white' for x in
                               [temp[i + 1][j], temp[i + 2][j], temp[i][j - 1]]):
                            copy = np.copy(temp)
                            copy[i][j] = copy[i + 1][j] \
                                = copy[i + 2][j] = copy[i][j - 1] = self.move_type
                            move_set.append(copy[2:-2, 2:-2].tolist())
                        if all(x == 'white' for x in
                               [temp[i + 1][j], temp[i][j + 1], temp[i][j + 2]]):
                            copy = np.copy(temp)
                            copy[i][j] = copy[i + 1][j] \
                                = copy[i][j + 1] = copy[i][j + 2] = self.move_type
                            move_set.append(copy[2:-2, 2:-2].tolist())
                        if all(x == 'white' for x in
                               [temp[i - 1][j], temp[i - 2][j], temp[i][j + 1]]):
                            copy = np.copy(temp)
                            copy[i][j] = copy[i - 1][j] \
                                = copy[i - 2][j] = copy[i][j + 1] = self.move_type
                            move_set.append(copy[2:-2, 2:-2].tolist())
                        if all(x == 'white' for x in
                               [temp[i - 1][j], temp[i][j - 1], temp[i][j - 2]]):
                            copy = np.copy(temp)
                            copy[i][j] = copy[i - 1][j] \
                                = copy[i][j - 1] = copy[i][j - 2] = self.move_type
                            move_set.append(copy[2:-2, 2:-2].tolist())
            # need to separately check all of these because multiple can be true simultaneously

        move_set.remove(initial)  # necessary in all cases coincidentally

        # this should remove the moves that have already been played
        for move in move_set:
            if self.in_previous_moves(move):
                move_set.remove(move)

        return move_set

    def make_move(self, initial: list, move: list) -> None:
        """This function makes a move."""
        move_set = self.get_valid_moves(initial)
        if move in move_set:
            # make the move?
            pass

    def _update_red_win_probability(self) -> None:
        pass
