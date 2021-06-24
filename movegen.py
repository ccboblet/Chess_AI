import board_reps as br

class MoveGen:
    def __init__(self):
        self.gen_map = {
            1 : self.rook_gen,
            2 : self.knight_gen,
            3 : self.bishop_gen,
            4 : self.queen_gen,
            5 : self.king_gen,
            6 : self.pawn_gen
        }

    def generate(self, position):
        color = 8 if position.turn == 1 else 0
        pieces = dict()
        moves = list()
        for i, j in enumerate(position.board):
            if j&8 == color and j != 0:
                pieces[i] = j
        for i in pieces:
            ptype = pieces[i]&7
            moves.extend(self.gen_map[ptype](position, i))
        return moves
    
    def rook_gen(self, position, loc):
        return []
    
    def knight_gen(self, position, loc):
        return []

    def bishop_gen(self, position, loc):
        return []

    def queen_gen(self, position, loc):
        return []
    
    def king_gen(self, position, loc):
        moves = list()
        dir = [0x10, 0x01, 0x11, 0x0f, 0x02]
        sign = [1,-1]
        for i in dir:
            for j in sign:
                stop = loc+i*j
                if self.in_board(stop):
                    capture = (position.board[loc]&8) ^ (position.board[stop]&8)
                    if capture or position.board[stop]==0:
                        moves.append(br.Move(loc,stop,position.board[loc]))
        return []
                    

    def pawn_gen(self, position, start):
        startline = {
            1 : range(0x10,0x18,1),
            -1: range(0x60,0x68,1)
        }
        finishline = {
            1 : range(0x70,0x78,1),
            -1: range(0x00,0x08,1)
        }
        diag = [0x0f,0x11]
        moves = list()
        sign = ((position.board[start]>>3)*(-2))+1

        # Check double moves
        if start in startline[sign]:
            stop = start+0x20*sign
            if self.in_board(stop):
                if position.board[stop] == 0:
                    moves.append(br.Move(start,stop,position.board[start]))
        
        # Check single push moves and promotion
        stop = start+0x10*sign
        if self.in_board(stop):
            if position.board[stop] == 0:
                moves.append(br.Move(start,stop,position.board[start]))

        # Check capture moves and promotion and enpassante
        for i in diag:
            stop = start+i*sign
            if self.in_board(stop):
                if (position.board[start]&8) ^ (position.board[stop]&8) and position.board[stop] != 0:
                    moves.append(br.Move(start,stop,position.board[start]))
        
        return moves
    
    def in_board(self, num):
        return False if (num&8) or (num&0x80) else True

if __name__ == "__main__":
    p = br.Board_0x88()
    p.turn = 1
    g = MoveGen()
    moves = g.generate(p)
    print(len(moves))