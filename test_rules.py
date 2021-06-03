import unittest
import rules
import board_reps as br

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
            move = br.Move(0,0x20,1)
            self.position.board[0x10] = 0
            self.rule.rook_rules(self.position,move)
            self.assertEqual(self.position.board[0x20],1)
            self.assertEqual(self.position.board[0x00],0)

            # Test rook cannot move through pieces
            self.rule.path = 0x20
            self.rule.sign = -1
            self.position = br.Board_0x88()
            move = br.Move(0x20,0,1)
            self.position.board[0x00] = 0
            self.position.board[0x20] = 1
            self.rule.rook_rules(self.position,move)
            self.assertEqual(self.position.board[0x00],0)
            self.assertEqual(self.position.board[0x20],1)

            # Test rook can capture
            self.rule.sign = 1
            self.rule.path = 0x60
            self.position = br.Board_0x88()
            move = br.Move(0,0x60,1)
            self.position.board[0x10] = 0
            self.rule.rook_rules(self.position,move)
            self.assertEqual(self.position.board[0x60],1)
            self.assertEqual(self.position.board[0x00],0)

            # Test illegal path
            self.rule.sign = -1
            self.rule.path = 0x9
            self.position = br.Board_0x88()
            move = br.Move(0x35,0x3e,1)
            self.position.board[0x35] = 1
            self.position.board[0] = 0
            self.rule.rook_rules(self.position,move)
            self.assertEqual(self.position.board[0x35],1)
            self.assertEqual(self.position.board[0x3e],0)

    def test_knight_rules(self):
            # Test knight move from starting position
            self.rule.path = 0x21
            self.rule.sign = 1
            self.position = br.Board_0x88()
            move = br.Move(1,0x21,2)
            self.rule.knight_rules(self.position,move)
            self.assertEqual(self.position.board[0x21],2)
            self.assertEqual(self.position.board[0x01],0)

            # Test illegal move
            self.rule.path = 0x20
            self.rule.sign = 1
            self.position = br.Board_0x88()
            move = br.Move(1,0x20,2)
            self.rule.knight_rules(self.position,move)
            self.assertEqual(self.position.board[0x01],2)
            self.assertEqual(self.position.board[0x20],0)

    def test_bishop_rules(self):
            # Test knight move from starting position
            self.rule.path = 0x33
            self.rule.sign = 1
            self.position = br.Board_0x88()
            move = br.Move(2,0x35,3)
            self.position.board[0x13] = 0
            self.rule.bishop_rules(self.position,move)
            self.assertEqual(self.position.board[0x35],3)
            self.assertEqual(self.position.board[0x02],0)

            # Test illegal move
            self.rule.path = 0x20
            self.rule.sign = 1
            self.position = br.Board_0x88()
            move = br.Move(1,0x20,2)
            self.rule.bishop_rules(self.position,move)
            self.assertEqual(self.position.board[0x02],3)
            self.assertEqual(self.position.board[0x20],0)

if __name__ == '__main__':
    unittest.main()