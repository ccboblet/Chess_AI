import board_reps as br

class MoveGen:
    '''
    Input:
    Position

    For each piece of a color
    Catagories:
    Push pieces
    Knights
    Kings
    Pawns
    Iterate over all directions
    Check each square for empty or capture
    Break on out of bounds or same color piece
    Break on different color after adding the move
    Append each move
    '''
    def __init__(self):
        self.gen_map = {
            1 : self.rook_gen,
            2 : self.knight_gen,
            3 : self.bishop_gen,
            4 : self.queen_gen,
            5 : self.king_gen,
            6 : self.pawn_gen
        }
    
        self.ends = [0x78,-1]

    def generate(self, position):
        color = 1 if position.turn == 1 else 0
        pieces = dict()
        moves = list()
        for i, j in enumerate(position.board):
            if self.get_color(j) == color and j:
                pieces[i] = j
        for i in pieces:
            ptype = pieces[i]&7
            moves.extend(self.gen_map[ptype](position, i))
        return moves
    
    def rook_gen(self, position, loc):
        moves = list()
        dir = [0x10, 0x01]
        sign = [1,-1]
        color = self.get_color(position.board[loc])
        for i in dir:
            for j in sign:
                for m in self.ends:
                    for n in range(loc+i*j,m,i*j):
                        if not self.in_board(n):
                            break
                        piece = position.board[n]
                        if piece:
                            if color != self.get_color(piece):
                                moves.append(br.Move(loc,n,position.board[loc]))
                            break
                        else:
                            moves.append(br.Move(loc,n,position.board[loc]))
        return moves
    
    def knight_gen(self, position, loc):
        moves = []
        dir = [0x21, 0x1f, 0x12, 0x0e]
        sign = [1,-1]
        color = self.get_color(position.board[loc])
        for i in dir:
            for j in sign:
                stop = loc+i*j
                if not self.in_board(stop):
                    continue
                piece = position.board[stop]
                if piece:
                    if self.get_color(piece) == color:
                        continue
                moves.append(br.Move(loc, stop, position.board[loc]))
                            
        return moves

    def bishop_gen(self, position, loc):
        moves = list()
        dir = [0x0f, 0x11]
        sign = [1,-1]
        color = self.get_color(position.board[loc])
        for i in dir:
            for j in sign:
                for m in self.ends:
                    for n in range(loc+i*j,m,i*j):
                        if not self.in_board(n):
                            break
                        piece = position.board[n]
                        if piece:
                            if color != self.get_color(piece):
                                moves.append(br.Move(loc,n,position.board[loc]))
                            break
                        else:
                            moves.append(br.Move(loc,n,position.board[loc]))
        return moves

    def queen_gen(self, position, loc):
        moves = list()
        dir = [0x10, 0x01, 0x0f, 0x11]
        sign = [1,-1]
        color = self.get_color(position.board[loc])
        for i in dir:
            for j in sign:
                for m in self.ends:
                    for n in range(loc+i*j,m,i*j):
                        if not self.in_board(n):
                            break
                        piece = position.board[n]
                        if piece:
                            if color != self.get_color(piece):
                                moves.append(br.Move(loc,n,position.board[loc]))
                            break
                        else:
                            moves.append(br.Move(loc,n,position.board[loc]))
        return moves
    
    def king_gen(self, position, loc):
        moves = list()
        dir = [0x10, 0x01, 0x11, 0x0f]
        sign = [1,-1]
        color = position.board[loc] >> 3 & 1
        for i in dir:
            for j in sign:
                stop = loc+i*j
                if self.in_board(stop):
                    scolor = position.board[stop] >> 3 & 1
                    if color != scolor:
                        moves.append(br.Move(loc,stop,position.board[loc]))
        return moves
                    
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
        return False if (num&0x08) or (num&0x80) else True
    
    def get_color(self, piece):
        return piece >> 3 & 1

if __name__ == "__main__":
    p = br.Board_0x88()
    gen = MoveGen()
    p.board[0x60] = 0
    p.board[0x50] = 14
    moves = gen.generate(p)
    print(len(moves))