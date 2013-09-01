__author__ = 'petastream'

import argparse

from game.character import Character
from game.map import Map


def parse_commandline():
    parser = argparse.ArgumentParser(description="Play Hunt the Wumpus.")

    parser.add_argument('--width', type=int, default=10, help="Width to use for map")
    parser.add_argument('--height', type=int, default=10, help="Height to use for map")

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_commandline()

    print("Building {0}x{1} map".format(args.width, args.height))

    map = Map(height=args.height, width=args.width, seed=1024)
    map.generate()
    #map.validate_layout()

    player = Character(name="Player")
    wumpus = Character(name="Wumpus")

    map.place_character(player)
    map.place_character(wumpus)

    print(map)