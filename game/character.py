__author__ = 'petastream'

from game import NORTH, EAST, SOUTH, WEST


class Character(object):
    def __init__(self, name):
        """
        Character initializer
        """
        self.name = name

    def move(self):
        """
        initiate move in given direction

        Uses PyDispatcher to notify the engine of move event
        """

    def __repr__(self):
        return self.name[0]