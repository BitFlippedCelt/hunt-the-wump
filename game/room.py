__author__ = 'petastream'

import json

from game import NORTH, EAST, SOUTH, WEST
from game import DIRECTIONS
from game import invert_direction, InvalidDirectionError


class NeighborExistsError(Exception):
    """
    NeighborExistsError is raised when trying to add a neighboring room using a direction already occupied by
    another room reference
    """
    def __init__(self, direction):
        self.message = "A neighbor already exists to the {0}".format(DIRECTIONS[direction])


class AddRoomAsOwnNeighborError(Exception):
    """
    AddRoomAsOwnNeighborError raised when trying to add room as neighbor of itself
    """
    def __init__(self):
        self.message = "Room may not be added as neighbor of itself."


class RoomAlreadyOccupiedError(Exception):
    """
    RoomAlreadyOccupiedError raised when the room is already occupied by a character
    """
    def __init__(self, character):
        self.character = character


class Room(object):
    EMPTY = 0
    PIT = 1
    TREASURE = 2
    BATS = 3

    ROOM_CODES = (
        " ",
        "P",
        "T",
        "B"
    )

    room_counter = 0

    def __init__(self, type=EMPTY):
        """
        Room object initializer.

        The Room object keeps a reference to it's neighbors internally
        """
        # _neighbors reference starts at the north neighbor and goes clockwise
        self.__neighbors = [None, None, None, None]
        self.__occupant = None
        self.__type = type
        self.room_id = Room.room_counter

        #Increment the room id so the next room has a unique id
        Room.room_counter += 1

    def add_neighbor(self, room, direction):
        """
        attach a neighboring room to this room instance.

        add_neighbor adds a reference to the passed in room at the index location specified by direction

        Keyword Arguments:
        room        -- Reference to the room object being assigned as a neighbor
        direction   -- Direction index to use when assigning neighbor (Room.NORTH,Room.EAST,Room.SOUTH,Room.WEST)
        """
        if room == self:
            raise AddRoomAsOwnNeighborError()

        try:
            if self.__neighbors[direction] is None:
                self.__neighbors[direction] = room
            else:
                raise NeighborExistsError(direction)
        except IndexError:
            raise InvalidDirectionError()

        # If room.get_neighbor is None then we call add_neighbor to reciprocate the relationship
        if room.get_neighbor(invert_direction(direction)) is None:
            room.add_neighbor(self, invert_direction(direction))

    def get_neighbor(self, direction):
        """
        get neighboring room in specified direction. Returns None if no room attached for requested direction

        Keyword Arguments:
        direction   -- Direction index to return room reference for
        """
        try:
            return self.__neighbors[direction]
        except IndexError:
            print("Invalid direction passed to get_neighbor method. {0} was the requested index.".format(direction))

    def get_neighbors(self):
        """
        get all neighboring rooms as tuple (North, East, South, West)
        """
        return self.__neighbors[NORTH], self.__neighbors[EAST], self.__neighbors[SOUTH], self.__neighbors[WEST]

    def occupy(self, character):
        """
        occupy room with character

        Keyword Arguments:
        character   -- Reference to the character to be placed in room

        Errors:
        RoomAlreadyOccupiedError    -- Raised when room is already occupied
        """
        if self.__occupant is None:
            self.__occupant = character
        else:
            raise RoomAlreadyOccupiedError(character=character)

    def remove_occupant(self, character=None):
        """
        remove occupant from the room

        Keyword Arguments:
        character   -- If specified only remove if occupant reference matches character reference
        """
        if character is None or self.__occupant == character:
            self.__occupant = None

    def __repr__(self):
        """
        Output room as string

         ---------
        |    D    |
        |D  P:G  D|
        |    D    |
         ---------

        D : Door
        P : Player
        W : Wumpus
        G : Gold
        T : Pit
        E : Entrance
        M : Mud
        """
        room_layout = []

        room_layout.append(" --------- ")
        room_layout.append("|    {0}    |".format("D" if self.get_neighbor(NORTH) is not None else " "))
        room_layout.append("| {0} {1}:{2} {3} |".format(
            "D" if self.get_neighbor(WEST) is not None else " ",
            self.__occupant.__repr__() if self.__occupant is not None else " ",
            Room.ROOM_CODES[self.__type],
            "D" if self.get_neighbor(EAST) is not None else " "
        ))
        room_layout.append("|    {0}    |".format("D" if self.get_neighbor(SOUTH) is not None else " "))
        room_layout.append(" --------- ")

        return "\n".join(room_layout)

    def __json__(self):
        """
        Output room as a JSON object
        """
        return json.dumps( {
            "id": self.__id,
            "neighbors": [room.room_id for room in self.__neighbors],
            "type": self.__type,
            "occupant": self.__occupant.character_id
        } )