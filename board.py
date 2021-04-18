import pygame
import numpy as np
from constants import *
from typing import Any, Optional


class Board:
    """This is the actual board object."""

    def __init__(self, board: list = STARTING_BOARD, previous_boards: list = [], is_red_move: bool = True,
                 move_type: str = 'red') -> None:
        """
        Init board function, players['red'] is the red player, players['blue'] is the blue player
        """
        self.board = board
        self.previous_boards = previous_boards
        self.is_red_move = is_red_move
        self.move_type = move_type

    def draw_board(self, window) -> None:
        """
        Draws the current board
        """
        window.fill(pygame.color.Color('white'))

        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.rect(window, pygame.color.Color('black'), (row * SQUARE_SIZE,
                                                                       col * SQUARE_SIZE,
                                                                       SQUARE_SIZE,
                                                                       SQUARE_SIZE), LINE_THICC)

    def draw_pieces(self, window) -> None:
        """We do this later"""

        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] == 'black':
                    rad = SQUARE_SIZE // 2 - LINE_THICC
                    center_pos = (
                        col * SQUARE_SIZE + SQUARE_SIZE / 2, row * SQUARE_SIZE + SQUARE_SIZE / 2)
                    pygame.draw.circle(window, pygame.color.Color('black'), center_pos, rad)
                else:
                    pygame.draw.rect(window, pygame.color.Color(self.board[row][col]),
                                     (col * SQUARE_SIZE + LINE_THICC,
                                      row * SQUARE_SIZE + LINE_THICC,
                                      SQUARE_SIZE - (2 * LINE_THICC),
                                      SQUARE_SIZE - (2 * LINE_THICC)), 0)

        self.previous_boards += self.board

    def get_valid_moves(self) -> list:
        """
        This function returns a list of lists with all possible moves calculated when given a board
        state, and whether it is red's move or not. THIS FUNCTION NEEDS TO USE PREVIOUS MOVE
        FUNCTION AND THEN REMOVE PREVIOUS STATES FROM POSSIBLE.

        Preconditions:
            - initial is represented in move notation

        >>> g = Board() # this should load a game tree with only the first position
        >>> len(g.get_valid_moves()) == 5
        True
        """
        move_set = []
        keep_searching = True
        if self.move_type == 'black':
            # do the neutral piece shuffle
            # now we scramble the holder pieces in every possible permutation, and add those as well
            temp = np.array(self.board)
            # 2 arrays where the top and bottom neutral pieces are removed respectively
            top_and_bottom = [temp.copy(), temp.copy()]
            # remove the top piece from top
            for i in range(len(temp)):
                for j in range(len(temp)):
                    if temp[i][j] == 'black' and keep_searching:
                        top_and_bottom[0][i][j] = 'white'
                        keep_searching = False

            # remove the bottom piece from bottom
            for i in range(len(temp)):
                for j in range(len(temp)):
                    if top_and_bottom[0][i][j] == 'black':
                        top_and_bottom[1][i][j] = 'white'

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
            temp = np.pad(np.array(self.board), pad_width=2, mode='constant',
                          constant_values='gray')

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
            # this should remove the moves that have already been played
            for move in move_set:
                if move in self.previous_boards:
                    move_set.remove(move)
            # need to separately check all of these because multiple can be true simultaneously

        move_set.remove(self.board)  # necessary in all cases coincidentally

        return move_set
