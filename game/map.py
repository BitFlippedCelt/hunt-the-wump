__author__ = 'petastream'

import random

from game import NORTH, EAST, SOUTH, WEST
from game.room import Room
from game.room import RoomAlreadyOccupiedError


class InvalidRoomReferenceError(Exception):
    """
    Raised when requested room reference does not exist on map
    """
    def __init__(self, room):
        self.room = room

class NoRoomAtCoordinatesError(Exception):
    """
    Raised when interacting with the map using coordinates that point to location without a room reference
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Map(object):
    def __init__(self, width=5, height=5, seed=42):
        """
        Map object initializer.

        The Map object generates and manages the interlinked rooms.

        Keyword Arguments:
        width   -- number of rooms wide the map can be
        height  -- number of rooms high the map can be
        seed    -- define the number used to seed the random number generator
        """
        self.rnd = random.Random()
        self.rnd.seed(seed)

        self.width = width
        self.height = height

        # Map state setup
        self.map = None
        self.__rooms = None

    def generate(self):
        """
        generate a new map layout.
        """
        self.map = [[None for x in range(self.height)] for y in range(self.width)]
        self.__rooms = []

        # Init self.map with newly instantiated Room objects
        for x in range(self.width):
            for y in range(self.height):
                if self.rnd.random() > 0.2:
                    room_type = Room.EMPTY

                    type_selector = self.rnd.random()
                    if 0.1 < type_selector < 0.15:
                        room_type = Room.PIT
                    elif 0.4 < type_selector < 0.5:
                        room_type = Room.TREASURE
                    elif 0.6 < type_selector < 0.65:
                        room_type = Room.BATS

                    room = Room(type=room_type)

                    self.map[x][y] = room
                    self.__rooms.append(room)

        # Add doors
        for x in range(1, self.width):
            for y in range(1, self.height):
                if self.map[x][y] is not None:
                    if self.rnd.random() >= 0.3:
                        if self.map[x-1][y] is not None:
                            self.map[x][y].add_neighbor(self.map[x-1][y], WEST)

                    if self.rnd.random() >= 0.3:
                        if self.map[x][y-1] is not None:
                            self.map[x][y].add_neighbor(self.map[x][y-1], NORTH)

        # Remove non connected rooms from map
        for x in range(self.width):
            for y in range(self.height):
                if self.map[x][y] is not None and \
                        self.map[x][y].get_neighbor(NORTH) is None and \
                        self.map[x][y].get_neighbor(EAST) is None and \
                        self.map[x][y].get_neighbor(SOUTH) is None and \
                        self.map[x][y].get_neighbor(WEST) is None:
                    self.__rooms.remove(self.map[x][y])
                    self.map[x][y] = None

        # Validate room layout
        groups = self.validate_layout()

        if len(groups) > 1:
            #self.__connect_room_groups(groups=groups)
            self.generate()
        else:
            print("Map generated with {0} rooms.".format(len(self.__rooms)))

    def __connect_room_groups(self, groups):
        print("{0} groups of rooms generated, attempting to connect groups.".format(len(groups)))

        for group in groups:
            group_rect = self.__get_group_extents(group)

    def __get_group_extents(self, group):
        """
        returns rectangle coordinates defining the bounding area of room group
        """
        x_min = self.width
        x_max = 0
        y_min = self.height
        y_max = 0
        for room in group:
            if room is not None:
                x, y = self.get_coordinates(room)

                if x < x_min: x_min = x
                elif x > x_max: x_max = x

                if y < y_min: y_min = y
                elif y > y_max: y_max = y

        return x_min, y_min, x_max, y_max

    def place_character(self, character, x=None, y=None):
        """
        Place character in room

        Keyword Arguments:
        character   -- Reference to the character being spawned
        x           -- x coordinate to spawn character at random if None
        Y           -- y coordinate to spawn character at random if None
        """

        if x is None or y is None:
            # Random
            room = random.choice(self.__rooms)
            try:
                room.occupy(character)
            except RoomAlreadyOccupiedError:
                self.place_character(character)
        else:
            # Coordinate based
            if self.map[x][y] is not None:
                for room in self.__rooms:
                    room.remove_occupant(character=character)

                self.map[x][y].occupy(character)
            else:
                raise NoRoomAtCoordinatesError(x, y)

    def validate_layout(self):
        """
        Validate that all rooms are accessible via a least a single pathway

        Runs group_attached on all rooms and generates a groups object which contains
        lists of all rooms that connect
        """
        groups = []

        for room in self.__rooms:
            # If room already processed as part of a group skip
            room_group = None
            for group in groups:
                if room in group:
                    room_group = group

            if room_group is None:
                room_group = self.group_attached(room, room_group)
                groups.append(room_group)

        return groups

    def group_attached(self, room, group=None):
        """
        recursively walk attached rooms and add them to group
        """
        if group is None:
            group = [room]

        for neighbor in room.get_neighbors():
            if neighbor is not None and neighbor not in group:
                group.append(neighbor)
                self.group_attached(neighbor, group)

        return group

    def get_coordinates(self, room):
        """
        Returns the x, y coordinates of the requested room
        """
        if room in self.__rooms:
            for x in range(self.width):
                for y in range(self.height):
                    if room == self.map[x][y]:
                        return x, y
        else:
            raise InvalidRoomReferenceError(room=room)

    def __repr__(self):
        """
        Returns textual grid showing the map layout
        """
        screen_buffer = [""] * (self.height * 5)
        for y in range(self.height):
            for x in range(self.width):
                if self.map[x][y] is not None:
                    rows = self.map[x][y].__repr__().split('\n')
                    for row_idx in range(5):
                        screen_buffer[5 * y + row_idx] = "{0}{1}".format(screen_buffer[5 * y + row_idx], rows[row_idx])

                else:
                    for row_idx in range(5):
                        screen_buffer[5 * y + row_idx] = "{0}{1}".format(screen_buffer[5 * y + row_idx], "           ")

        return "\n".join(screen_buffer)
