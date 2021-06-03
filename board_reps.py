import numpy as np

# This speeds up checking for pieces wraping around the sides of the board
# Got inspiration for formatting from https://www.youtube.com/watch?v=7fzKxGRDFzE&ab_channel=CodeMonkeyKing
class Board_0x88:
    def __init__(self):
        # Each entry represents a square
        # The values on the left board represent pieces
        # White pice&8=1 bit black piece&8=0
        # 0 = rook, 1 = knight, 2 = bishop, 3 = queen, 4 = king, 5 = pawn
        # The values on the right board have yet to be determined
        self.board = np.array([
            1,   2,   3,   4,   5,   3,   2,   1,      0,0,0,0,0,0,0,0,
            6,   6,   6,   6,   6,   6,   6,   6,      0,0,0,0,0,0,0,0,
            0,   0,   0,   0,   0,   0,   0,   0,      0,0,0,0,0,0,0,0,
            0,   0,   0,   0,   0,   0,   0,   0,      0,0,0,0,0,0,0,0,
            0,   0,   0,   0,   0,   0,   0,   0,      0,0,0,0,0,0,0,0,
            0,   0,   0,   0,   0,   0,   0,   0,      0,0,0,0,0,0,0,0,
            14,  14,  14,  14,  14,  14,  14,  14,     0,0,0,0,0,0,0,0,
            9,   10,  11,  12,  13,  11,  10,  9,      0,0,0,0,0,0,0,0,
        ])
        self.board = self.board.astype(np.uint8)
        # 2 sets of 2 for each castle 
        # 1 => able to castle, 0 => unable to castle 
        # if the king move then both are set to 0
        self.castleflag = np.uint8(0b1111)
        # When a pawn double moves set the en passant square
        self.enpassant = np.uint8(0)
        # Move 1 = white, 0 = black
        self.turn = np.uint8(0b1)
        # Set a flag for promotion
        self.promotion = np.uint8(255)

class Move:
    def __init__(self, start, stop, piece_id):
        self.start = start
        self.stop = stop
        self.piece_id = piece_id