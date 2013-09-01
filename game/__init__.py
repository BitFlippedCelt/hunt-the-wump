__author__ = 'petastream'

# Directional
NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

DIRECTIONS = ("North", "East", "South", "West")


class InvalidDirectionError(Exception):
    pass


def invert_direction(direction):
    """
    Returns the opposite direction of passed direction
    """
    if direction == NORTH:
        return SOUTH
    elif direction == SOUTH:
        return NORTH
    elif direction == EAST:
        return WEST
    elif direction == WEST:
        return EAST
    else:
        raise InvalidDirectionError()