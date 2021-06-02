import numpy as np

# This class takes in a position and a move and outputs the new position
# The format for the position is undecided.
# Its fine if the format is bulky (takes lots of bits) as long as it evaluates fast

# Do not need the same rules for the ai? 

# The return needs to indicate promotion when necessary

class rules:
    def __init__(self):
        self.right = range(0,64,8)
        self.left = range(7,64,8)

    def update_position(self):
        if self.position.enpassant != self.move.stop:
            self.position.enpassant = np.uint8(0)
        if self.move.stop in self.position.pieces:
            captured = np.where(self.position.pieces == self.move.stop)
            for i in captured[0]:
                if i>15:
                    self.position.pieces[i] = self.position.pieces[28]
                else:
                    self.position.pieces[i] = self.position.pieces[4]
        for i in range(0,32):
            if self.position.pieces[i] == self.move.start:
                self.position.pieces[i] = self.move.stop

    def rook_rules(self):
        # find path
        # find collisions
        if abs(self.path) % 8 == 0:
            #up or down
            for i in range(self.move.start+8*self.sign,self.move.stop,8*self.sign):
                if i in self.position.pieces:
                    return False
        elif abs(self.path)<8:
            if self.sign<0 and self.move.start in self.right:
                return False
            if self.sign>0 and self.move.start in self.left:
                return False
            for i in range(self.move.start+self.sign,self.move.stop,self.sign):
                if i in self.right or i in self.left:
                    return False
                if i in self.position.pieces:
                    return False
        else:
            return False
        self.update_position()
        if self.move.piece_id==0:
            self.position.castleflag &= 0b0111
        elif self.move.piece_id==7:
            self.position.castleflag &= 0b1011
        elif self.move.piece_id==24:
            self.position.castleflag &= 0b1101
        elif self.move.piece_id==31:
            self.position.castleflag &= 0b1110
        return True
            
    def knight_rules(self):
        # 15 17 10 6 and negs
        if (self.move.start // 8) == (self.move.stop // 8):
            return False
        if self.move.start in self.right and self.move.stop in self.left:
            return False
        if self.move.start in self.left and self.move.stop in self.right:
            return False
        if self.move.start in self.right and self.move.stop in self.left:
            return False
        if abs(self.path) in [15,17,10,6]:
            self.update_position()
            return True
        else:
            return False

    def bishop_rules(self):
        if abs(self.path) % 7 == 0:
            if self.sign<0 and self.move.stop in self.right:
                return False
            elif self.sign>0 and self.move.stop in self.left:
                return False
            for i in range(self.move.start+7*self.sign,self.move.stop,7*self.sign):
                if i in self.right or i in self.left:
                    return False
                if i in self.position.pieces:
                    return False
        elif abs(self.path) % 9 == 0:
            if self.sign>0 and self.move.stop in self.right:
                return False
            elif self.sign<0 and self.move.stop in self.left:
                return False
            for i in range(self.move.start+9*self.sign,self.move.stop,9*self.sign):
                if i in self.right or i in self.left:
                    return False
                if i in self.position.pieces:
                    return False
        else:
            return False
        self.update_position()
        return True
    
    def king_rules(self):
        # if castle flag
        # if no collision
        # if correct direction
        # if correct distance
        bl = self.path == -2 and (self.position.castleflag and 0b1000) and self.move.piece_id==28
        br = self.path == 2 and (self.position.castleflag and 0b0100) and self.move.piece_id==28
        wl = self.path == -2 and (self.position.castleflag and 0b0010) and self.move.piece_id==4
        wr = self.path == 2 and (self.position.castleflag and 0b0001) and self.move.piece_id==4
        if bl or br or wl or wr:
            # Check for collision
            for i in range(self.move.start+self.sign,self.move.stop,self.sign):
                if i in self.position.pieces:
                    return False
            else:
                self.update_position()
                stop = self.move.stop
                self.move.start = stop+self.sign+(self.path-2)/4
                self.move.stop = stop-self.sign
                self.update_position()
            if self.move.piece_id<16:
                self.position.castleflag &= 0b0011
            else:
                self.position.castleflag &= 0b1100
            return True

        if abs(self.path) in [1,7,8,9]:
            if self.move.start in self.right and self.move.stop in self.left:
                return False
            if self.move.start in self.left and self.move.stop in self.right:
                return False
            self.update_position()
            if self.move.piece_id<16:
                self.position.castleflag &= 0b0011
            else:
                self.position.castleflag &= 0b1100
            return True
        else:
            return False

    def queen_rules(self):
        if self.rook_rules() or self.bishop_rules():
            return True
        else:
            return False

    def pawn_rules(self):
        if self.move.start in self.right and self.move.stop in self.left:
            return False
        if self.move.start in self.left and self.move.stop in self.right:
            return False

        if abs(self.path) == 16:
            for i in range(self.move.start+8*self.sign,self.move.stop+8*self.sign,8*self.sign):
                if i in self.position.pieces:
                    return False
        if self.move.piece_id < 16:
            if self.path == 16 and self.move.start<16:
                self.position.enpassant = self.move.stop
            elif self.path in [7,9] and self.move.stop in self.position.pieces:
                pass
            elif self.path in [7,9] and self.move.stop-self.position.enpassant ==  8:
                self.move.stop = self.position.enpassant
                self.update_position()
                self.move.stop = self.position.enpassant+8
                self.move.start = self.position.enpassant
            elif (self.path==8) and (self.move.stop not in self.position.pieces):
                pass
            else:
                return False

        elif self.move.piece_id > 15:
            if self.path == -16 and self.move.start>=48:
                self.position.enpassant = self.move.stop
            elif self.path in [-7,-9] and self.move.stop in self.position.pieces:
                pass
            elif self.path in [-7, -9] and self.move.stop-self.position.enpassant==-8:
                self.move.stop = self.position.enpassant
                self.update_position()
                self.move.stop = self.position.enpassant-8
                self.move.start = self.position.enpassant
            elif (self.path==-8) and (self.move.stop not in self.position.pieces):
                pass
            else:
                return False
        if self.move.stop<8 or self.move.stop>55:
            if self.move.stop == self.position.pieces[4] or self.move.stop == self.position.pieces[28]:
                pass
            else:
                self.promotion()
        self.update_position()
        return True

    def find_checks(self):
        if self.position.move == 0:
            king = 4
            enemy = range(16,32)
            enemy_king = 28
        else:
            king = 28
            enemy = range(0,16)
            enemy_king = 4
        # check if each piece can cause the a check
        # recursion! also promotion?
        for i in enemy:
            if i != enemy_king and self.position.pieces[i] == self.position.pieces[enemy_king]:
                continue
            start = self.position.pieces[i]
            stop = self.position.pieces[king]
            piece_id = i
            self.move = Move(start,stop,piece_id)
            if self.check_move():
                self.takeback()
                return False
            else:
                self.takeback()
                continue
        return True

    def save_position(self):
        temp = Position()
        temp.import_position(self.position)
        self.history.append(temp)

    def takeback(self):
        self.position = self.history[-1]
        self.history.pop(-1)

class Move:
    def __init__(self, start, stop, piece_id):
        self.start = start
        self.stop = stop
        self.piece_id = piece_id

class Position:
    def __init__(self):
        # Each number represents a square and each index corresponds to a piece
        self.pieces = np.uint8([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63])
        # 2 sets of 2 for each castle 
        # 1 = able to castle
        # if the king move then both are set to 0
        self.castleflag = 0b1111
        # When a pawn double moves set the en passant square
        self.enpassant = np.uint8(0)
        # Move 1 = white, 0 = black
        self.move = 0b1

    def import_position(self, position):
        self.pieces = np.copy(position.pieces)
        self.castleflag = position.castleflag
        self.enpassant = position.enpassant
        self.move = position.move