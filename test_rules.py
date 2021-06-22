from operator import pos
import unittest

from numpy.testing._private.utils import assert_equal
import rules
import board_reps as br
from unittest.mock import MagicMock


class TestRules(unittest.TestCase):
    # Create rules class and init dicts
    @classmethod
    def setUpClass(cls):
        cls.rule = rules.Rules()

    def test_make_move(self):
        rule = rules.Rules()
        position = br.Board_0x88()
        rule.check_move = MagicMock()
        rule.check_move.return_value = br.B88_Blank(position)
        rule.find_checks = MagicMock()
        move = MagicMock()
        rule.make_move(position, move)
        rule.check_move.assert_called()
        rule.find_checks.assert_called()

    def test_check_move(self):
        rule = rules.Rules()
        rule.rule_map[2] = MagicMock()
        rule.rule_map[4] = MagicMock()

        rule.path = 0x21
        rule.sign = 1
        position = br.Board_0x88()
        move = br.Move(0x01, 0x22, 2)
        rule.check_move(position, move)
        rule.rule_map[2].assert_called()

        rule.path = 0x30
        rule.sign = 1
        position = br.Board_0x88()
        move = br.Move(0x03,0x33, 4)
        rule.check_move(position, move)
        rule.rule_map[4].assert_called()

    def test_rook_rules(self):
        # Test rook move forward 2 squares
        self.rule.path = 0x20
        self.rule.sign = 1
        self.position = br.Board_0x88()
        move = br.Move(0, 0x20, 1)
        self.position.board[0x10] = 0
        self.rule.rook_rules(self.position, move)
        self.assertEqual(self.position.board[0x20], 1)
        self.assertEqual(self.position.board[0x00], 0)

        # Test rook cannot move through pieces
        self.rule.path = 0x20
        self.rule.sign = -1
        self.position = br.Board_0x88()
        move = br.Move(0x20, 0, 1)
        self.position.board[0x00] = 0
        self.position.board[0x20] = 1
        self.rule.rook_rules(self.position, move)
        self.assertEqual(self.position.board[0x00], 0)
        self.assertEqual(self.position.board[0x20], 1)

        # Test rook can capture
        self.rule.sign = 1
        self.rule.path = 0x60
        self.position = br.Board_0x88()
        move = br.Move(0, 0x60, 1)
        self.position.board[0x10] = 0
        self.rule.rook_rules(self.position, move)
        self.assertEqual(self.position.board[0x60], 1)
        self.assertEqual(self.position.board[0x00], 0)

        # Test illegal path
        self.rule.sign = -1
        self.rule.path = 0x9
        self.position = br.Board_0x88()
        move = br.Move(0x35, 0x3e, 1)
        self.position.board[0x35] = 1
        self.position.board[0] = 0
        self.rule.rook_rules(self.position, move)
        self.assertEqual(self.position.board[0x35], 1)
        self.assertEqual(self.position.board[0x3e], 0)

    def test_knight_rules(self):
        # Test knight move from starting position
        self.rule.path = 0x21
        self.rule.sign = 1
        self.position = br.Board_0x88()
        move = br.Move(1, 0x21, 2)
        self.rule.knight_rules(self.position, move)
        self.assertEqual(self.position.board[0x21], 2)
        self.assertEqual(self.position.board[0x01], 0)

        # Test illegal move
        self.rule.path = 0x20
        self.rule.sign = 1
        self.position = br.Board_0x88()
        move = br.Move(1, 0x20, 2)
        self.rule.knight_rules(self.position, move)
        self.assertEqual(self.position.board[0x01], 2)
        self.assertEqual(self.position.board[0x20], 0)

    def test_bishop_rules(self):
        # Test bishop move from starting position
        self.rule.path = 0x33
        self.rule.sign = 1
        self.position = br.Board_0x88()
        move = br.Move(2, 0x35, 3)
        self.position.board[0x13] = 0
        self.rule.bishop_rules(self.position, move)
        self.assertEqual(self.position.board[0x35], 3)
        self.assertEqual(self.position.board[0x02], 0)

        # Test illegal move
        self.rule.path = 0x20
        self.rule.sign = 1
        self.position = br.Board_0x88()
        move = br.Move(1, 0x20, 2)
        self.rule.bishop_rules(self.position, move)
        self.assertEqual(self.position.board[0x02], 3)
        self.assertEqual(self.position.board[0x20], 0)

    def test_queen_rules(self):
        rule = rules.Rules()
        rule.bishop_rules = MagicMock()
        rule.rook_rules = MagicMock()

        # Test queen rook move
        rule.path = 0x30
        rule.sign = 1
        self.position = br.Board_0x88()
        move = br.Move(0x03, 0x33, 4)
        self.position.board[0x013] = 0
        rule.queen_rules(self.position, move)
        rule.rook_rules.assert_called_with(self.position, move)

        # Test queen bishop move
        rule.path = 0x33
        rule.sign = 1
        self.position = br.Board_0x88()
        move = br.Move(0x03,0x36,4)
        self.position.board[0x14] = 0
        rule.queen_rules(self.position,move)
        rule.bishop_rules.assert_called_with(self.position, move)

    def test_king_rules(self):
        # Test king move from starting position
        self.rule.path = 0x01
        self.rule.sign = 1
        self.position = br.Board_0x88()
        move = br.Move(0x04, 0x05, 5)
        self.position.board[0x05] = 0
        self.rule.king_rules(self.position, move)
        self.assertEqual(self.position.board[0x05], 5)
        self.assertEqual(self.position.board[0x04], 0)

        # Check illegal move
        self.rule.path = 0x03
        self.rule.sign = 1
        self.position = br.Board_0x88()
        move = br.Move(0x04, 0x07, 5)
        self.position.board[0x05] = 0
        self.position.board[0x06] = 0
        self.position.board[0x07] = 0
        self.rule.king_rules(self.position, move)
        self.assertEqual(self.position.board[0x07], 0)
        self.assertEqual(self.position.board[0x04], 5)

        # Check castle
        self.rule.path = 0x02
        self.rule.sign = -1
        self.position = br.Board_0x88()
        move = br.Move(0x04, 0x02, 5)
        self.position.board[0x03] = 0
        self.position.board[0x02] = 0
        self.position.board[0x01] = 0
        self.rule.king_rules(self.position, move)
        self.assertEqual(self.position.board[0x04], 0)
        self.assertEqual(self.position.board[0x03], 1)
        self.assertEqual(self.position.board[0x02], 5)
    
    def test_pawn_rules(self):
        # Test pawn double move
        self.rule.path = 0x020
        self.rule.sign = 1
        self.position = br.Board_0x88()
        move = br.Move(0x011, 0x031, 6)
        self.rule.pawn_rules(self.position, move)
        self.assertEqual(self.position.board[0x31], 6)
        self.assertEqual(self.position.board[0x11], 0)

    def test_find_checks(self):
        rule = rules.Rules()
        position = br.Board_0x88()
        position = br.B88_Blank(position)
        position.board[0x40] = 5
        position.board[0x50] = 9
        position.turn = 1
        temp = rule.find_checks(position)
        self.assertEqual(temp, False)
if __name__ == '__main__':
    unittest.main()
