import unittest
from unittest.mock import patch
from Items_classes import Board
from Player_classes import Dog, Cat, Rat


class BoardTest(unittest.TestCase):

    def setUp(self):
        self.board1 = Board(5, 7)
        self.board2 = Board(7, 3)
        self.board3 = Board(2, 2)

    def test_lh(self):
        self.assertEqual(self.board1.l, 5)
        self.assertEqual(self.board2.l, self.board1.h)
        self.assertNotEqual(self.board2.h, self.board1.h)
        self.assertGreater(self.board1.h, self.board1.l)
        # if l or h in constructor is less than 5, is set up to 5
        self.assertEqual(self.board2.h, 5)
        self.assertEqual(self.board3.l, 5)
        self.assertNotEqual(self.board3.l, 2)

    def test_board(self):
        self.assertEqual(self.board3.table, Board(5, 5).table)
        self.assertNotEqual(self.board1.table, self.board2.table)

    def test_items(self):
        # board1 has bigger 'area' than board3, so there are more enemies
        self.assertGreaterEqual(len(self.board1.enemies), len(self.board3.enemies))
        # always more enemies than weapons and meds
        self.assertGreater(len(self.board1.enemies), len(self.board3.weapons))
        self.assertGreater(len(self.board2.enemies), len(self.board2.meds))
        # no items' coordinates outside the table
        self.assertNotIn((5, 5), self.board1.weapons)
        # coordinates can't be negative
        self.assertNotIn((-1, -2), self.board1.enemies)


class PlayersTest(unittest.TestCase):

    def setUp(self):
        self.board1 = Board(5, 10)
        self.rat = Rat(self.board1)
        self.cat = Cat(self.board1)
        self.dog = Dog(self.board1)

    def test_coordinates(self):
        # starting coordinates depends on table size (same for every Player subclass)
        self.assertEqual((self.rat.x, self.rat.y), (self.board1.l // 2, self.board1.h // 2))
        self.assertEqual((self.cat.x, self.cat.y), (2, 5))

    def test_moves(self):
        self.dog.move_up()
        self.assertEqual((self.dog.px, self.dog.py), (self.board1.l // 2, self.board1.h // 2))
        self.assertNotEqual((self.dog.px, self.dog.py), (self.dog.x, self.dog.y))
        self.assertEqual((self.dog.px, self.dog.py - 1), (self.dog.x, self.dog.y))
        self.dog.move_right()
        self.assertEqual((self.dog.px + 1, self.dog.py), (self.dog.x, self.dog.y))
        self.dog.move_left()
        self.assertEqual((self.dog.px - 1, self.dog.py), (self.dog.x, self.dog.y))
        self.dog.move_down()
        self.assertEqual((self.dog.px, self.dog.py + 1), (self.dog.x, self.dog.y))

    coordinates = '1 3'

    @patch('builtins.input', return_value=coordinates)
    def test_rat(self, mock_input):
        self.rat.superpower()
        self.assertEqual(self.rat.x, 1)
        self.assertEqual(self.rat.y, 3)

    def test_cat(self):
        self.cat.superpower()
        for e in self.board1.enemies.keys():
            self.assertEqual(self.board1.table[e[1]][e[0]], 'x')

    a = '1'

    @patch('builtins.input', return_value=a)
    def test_dog1(self, mock_input):
        self.dog.superpower()
        for e in self.board1.meds.keys():
            self.assertEqual(self.board1.table[e[1]][e[0]], 'O')

    a = '2'

    @patch('builtins.input', return_value=a)
    def test_dog2(self, mock_input):
        self.dog.superpower()
        for e in self.board1.weapons.keys():
            self.assertEqual(self.board1.table[e[1]][e[0]], 'O')


if __name__ == "__main__":
    unittest.main()

