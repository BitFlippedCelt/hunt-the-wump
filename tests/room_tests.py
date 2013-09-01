__author__ = 'petastream'

import unittest
from game.room import NeighborExistsError, AddRoomAsOwnNeighborError, InvalidDirectionError, Room


class TestRoom(unittest.TestCase):
    def setUp(self):
        pass

    def test_add_neighbor_raises_neighbor_exists_error_when_adding_to_occupied_direction(self):
        first = Room()
        second = Room()
        third = Room()

        first.add_neighbor(room=second, direction=Room.EAST)
        first.add_neighbor(room=third, direction=Room.NORTH)

        self.assertRaises(NeighborExistsError, first.add_neighbor, room=third, direction=Room.EAST)

    def test_add_neighbor_raises_add_room_as_own_neighbor_error(self):
        first = Room()

        self.assertRaises(AddRoomAsOwnNeighborError, first.add_neighbor, room=first, direction=Room.NORTH)

    def test_get_neighbor_returns_correct_room_reference_after_add_neighbor(self):
        first = Room()
        second = Room()

        first.add_neighbor(second, Room.SOUTH)
        room_a = first.get_neighbor(Room.SOUTH)
        room_b = second.get_neighbor(Room.NORTH)

        self.assertIsNotNone(room_a, "First's neighbor is None")
        self.assertIsNotNone(room_b, "Second's neighbor is None")
        self.assertEqual(second, room_a, "First's neighbor is not equal to second's reference.")
        self.assertEqual(first, room_b, "Second's neighbor is not equal to first's reference.")

    def test_invert_direction_raises_invalid_direction_error(self):
        first = Room()

        self.assertRaises(InvalidDirectionError, first.invert_direction, direction=10)

    def test_add_neighbor_raises_invalid_direction_error(self):
        first = Room()

        self.assertRaises(InvalidDirectionError, first.add_neighbor, room=Room(), direction=10)


if __name__ == "__main__":
    unittest.main()