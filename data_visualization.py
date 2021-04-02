"""
This file is for visualizing the sample games and testing to see if the csv files are being read.
"""
import csv


def print_sample(games_file: str) -> None:
    '''
    This is meant to be run on sample_game.csv to quickly look at it in string format.
    :param games_file:
    :return:
    '''
    with open(games_file) as csv_file:
        reader = csv.reader(csv_file)

        for row in reader:
           for i in range(len(row)):
               if i % 4 == 0 and i != 0:
                   print('\n')
               print(row[i])
