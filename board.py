import pygame
import player
import numpy as np
from constants import *
from gametree import GameTree
from typing import Any, Optional


class Board:
    """This is the actual board object."""

    def __init__(self, players: dict[str, Any]) -> None:
        """
        Init board function, players['red'] is the red player, players['blue'] is the blue player
        """
        self.board = STARTING_BOARD
        self.previous_boards = []
        self.is_red_move = True
        self.move_type = 'red'
        self.players = players

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

        for col in range(COLS):
            for row in range(ROWS):
                if self.board[col][row] == 'black':
                    rad = SQUARE_SIZE // 2 - LINE_THICC
                    center_pos = (
                        col * SQUARE_SIZE + SQUARE_SIZE / 2, row * SQUARE_SIZE + SQUARE_SIZE / 2)
                    pygame.draw.circle(window, pygame.color.Color('black'), center_pos, rad)
                else:
                    pygame.draw.rect(window, pygame.color.Color(self.board[col][row]),
                                     (row * SQUARE_SIZE + LINE_THICC,
                                      col * SQUARE_SIZE + LINE_THICC,
                                      SQUARE_SIZE - (2 * LINE_THICC),
                                      SQUARE_SIZE - (2 * LINE_THICC)), 0)

        self.previous_boards += self.board

    def check_board(self, new_board: list[list], g: GameTree) -> bool:
        """
        Checks if the next move (therefore the next board state) is not in previous_boards, a list
        containing all previously achieved board states
        """
        if new_board in g.get_valid_moves(new_board):
            return True
        else:
            return False

    def draw_move(self, new_board: list[list], g: GameTree, window):
        """
        This function draws a move.
        """
        if self.check_board(new_board, g):
            self.board = new_board
            self.draw_pieces(window)
        else:
            print('This is not a legal move.')

    def get_valid_moves(self) -> list:
        """
        This function returns a list of lists with all possible moves calculated when given a board
        state, and whether it is red's move or not. THIS FUNCTION NEEDS TO USE PREVIOUS MOVE
        FUNCTION AND THEN REMOVE PREVIOUS STATES FROM POSSIBLE.

        Preconditions:
            - initial is represented in move notation

        >>> g = Board({'red': player.RandomPlayer, 'blue': player.RandomPlayer}) # this should load a game tree with only the first position
        >>> len(g.get_valid_moves()) == 5
        True
        """
        move_set = []
        if self.move_type == 'black':
            # do the neutral piece shuffle
            # now we scramble the holder pieces in every possible permutation, and add those as well
            temp = np.array(self.board)
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
            temp = np.pad(np.array(self.board), pad_width=2, mode='constant', constant_values='gray')

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

        move_set.remove(self.board)  # necessary in all cases coincidentally

        # this should remove the moves that have already been played
        for move in move_set:
            if move in self.previous_boards:
                move_set.remove(move)

        return move_set

    def play_game(self, window):
        """ This function plays the game. """

        move_set = self.get_valid_moves()
        while len(move_set) != 0:
            # finds the player for this turn
            curr_player = self.players[self.move_type]
            # receives l-move from player
            l_move = curr_player.make_move(move_set)
            # changes board parameters to match move made by player and updates visual
            self.board = l_move
            self.move_type = 'black'
            self.draw_pieces(window)
            # determines possible neutral-move set and receives neutral-move from player
            move_set = self.get_valid_moves()
            neutral_move = curr_player.make_move(move_set)
            # changes board parameters to match move made by player and updates visual
            self.board = neutral_move
            self.is_red_move = not self.is_red_move
            if self.is_red_move:
                self.move_type = 'red'
            else:
                self.move_type = 'blue'
            self.draw_pieces(window)
            # determines possible l-moves for next turn to check if the game can continue
            move_set = self.get_valid_moves()

        # Once the while loop ends, we declare the winner to be whoever's turn it is not right now
        # After this, we can return the total move list as well as who won to make game trees
