"""
This file is for visualizing the sample games and testing to see if the csv files are being read.
"""
import csv
from player import *


def print_sample(games_file: str) -> None:
    """
    This is meant to be run on sample_game.csv to quickly look at it in string format.
    It is key to note that the sample_game is the black piece move, after red/blue pieces have moved
    :param games_file:
    :return:
    """
    with open(games_file) as csv_file:
        reader = csv.reader(csv_file)

        for row in reader:
            for i in range(len(row)):
                if i % 4 == 0 and i != 0:
                    print('\n')
                print(row[i])


def battle_royal(player1: Player, player2: Player) -> None:
    """
    This function has to AI's play against each other and plots the result of their games.
    """
    return None
