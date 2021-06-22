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
        self.enpassant = np.uint8(255)
        # Move 1 = white, 0 = black
        self.turn = np.uint8(0b1)
        # Set a flag for promotion
        self.promotion = np.uint8(255)

def B88_to_Print(b88):
    # Create a dict of piece_id(0-11) : square(0-63)
    position = {}
    for i in range(0x0,0x80,0x10):
        for j in range(8):
            if b88.board[i+j]:
                square = (i>>1)+j
                piece_id = b88.board[i+j]
                piece_id = piece_id - 1 - max(0,(piece_id&0x8)-6)
                position[square] = piece_id
    return position

def B88_Blank(b88):
    for i, j in enumerate(b88.board):
        b88.board[i] = 0
    b88.castleflag = 0
    b88.enpassant = 255
    b88.turn = 1
    b88.promotion = 255
    return b88

class Move:
    def __init__(self, start, stop, piece_id):
        self.start = start
        self.stop = stop
        self.piece_id = piece_id