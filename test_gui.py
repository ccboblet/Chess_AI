import unittest
import rules

class TestRules(unittest.TestCase):
    # Create rules class and init dicts
    @classmethod
    def setUpClass(cls):
        cls.rule = rules.Rules()
    
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
