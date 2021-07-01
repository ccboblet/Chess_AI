import unittest
import movegen as mg
import board_reps as br
from unittest.mock import MagicMock


class TestRules(unittest.TestCase):
    # Create rules class and init dicts
    @classmethod
    def setUpClass(cls):
        cls.movegen = mg.MoveGen()

    def test_generate(self):
        self.assertEqual(1,1)

    def test_rook_gen(self):
        position = br.Board_0x88()
        position = br.B88_Blank(position)
        position.board[0x44] = 9
        moves = self.movegen.rook_gen(position, 0x44)
        self.assertEqual(len(moves), 14)

    def test_knight_gen(self):
        position = br.Board_0x88()
        position = br.B88_Blank(position)
        position.board[0x44] = 10
        moves = self.movegen.knight_gen(position, 0x44)
        self.assertEqual(len(moves), 8)

    def test_bishop_gen(self):
        position = br.Board_0x88()
        position = br.B88_Blank(position)
        position.board[0x44] = 11
        moves = self.movegen.bishop_gen(position, 0x44)
        self.assertEqual(len(moves), 13)

    def test_queen_gen(self):
        position = br.Board_0x88()
        position = br.B88_Blank(position)
        position.board[0x44] = 12
        moves = self.movegen.queen_gen(position, 0x44)
        self.assertEqual(len(moves), 27)

    def test_king_gen(self):
        position = br.Board_0x88()
        position = br.B88_Blank(position)
        position.board[0x44] = 13
        moves = self.movegen.king_gen(position, 0x44)
        self.assertEqual(len(moves), 8)

    def test_pawn_gen(self):
        position = br.Board_0x88()
        position = br.B88_Blank(position)
        position.board[0x44] = 14
        moves = self.movegen.pawn_gen(position, 0x44)
        self.assertEqual(len(moves), 1)

    def test_in_board(self):
        test = self.movegen.in_board(0x11)
        self.assertEqual(test, True)

        test = self.movegen.in_board(0x19)
        self.assertEqual(test, False)

    def test_get_color(self):
        test = self.movegen.get_color(9)
        self.assertEqual(test,1)

        test = self.movegen.get_color(1)
        self.assertEqual(test,0)

if __name__ == '__main__':
    unittest.main()
