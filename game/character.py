__author__ = 'petastream'

import json


class Character(object):
    character_counter = 0

    def __init__(self, name):
        """
        Character initializer
        """
        self.name = name
        self.inventory = []

        self.character_id = Character.character_counter

        Character.character_counter += 1

    def move(self):
        """
        initiate move in given direction

        Uses PyDispatcher to notify the engine of move event
        """
        pass

    def __repr__(self):
        return self.name[0]

    def __json__(self):
        return json.dumps(
            {
                "id": self.character_id,
                "name": self.name,
                "inventory": self.inventory
            }
        )