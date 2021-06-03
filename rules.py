from operator import pos
import numpy as np
from copy import copy

# This class takes in a position and a move and outputs the new position
# The format for the position is undecided.
# Its fine if the format is bulky (takes lots of bits) as long as it evaluates fast

# Board representation - start with 0x88
# 16x8 1 byte array what do I store in side board
# Ideas: positional value, valid movement, bit board? 

# The return needs to indicate promotion when necessary

class Rules:
    def __init__(self):
        self.rule_map = {
            1 : self.rook_rules,
            2 : self.knight_rules,
            3 : self.bishop_rules,
            4 : self.queen_rules,
            5 : self.king_rules,
            6 : self.pawn_rules
        }

        self.castle_map = {
            0    : 0b0111,
            7    : 0b1011,
            4    : 0b0011,
            0x70 : 0b1101,
            0x77 : 0b1110,
            0x74 : 0b1100
        }

    # Checks for illegal capture
    # If it is a legal move - 
    #   updates turn, en passant
    #   returns new position
    # If it is an illegal move - 
    #   returns current position

    # Legal move qualifications
    # Capture
    # Path collision
    # Check
    def check_move(self, position, move):
        piece = position[move.start]
        dest = position[move.stop]
        if piece&8 ^ dest&8:
            self.path = move.start-move.stop if move.start>move.stop else move.stop-move.start
            self.sign = (move.start-move.stop)/self.path
            new = copy(position)
            new = self.rule_map[piece&7](new, move)
            if self.find_checks(new):
                new.enpassant = move.stop
                new.turn ^= 1
                position = new
        return position

    def rook_rules(self, position, move):
        # find path
        # find collisions
        # update castles
        if self.path % 0x10 == 0:
            step = 0x10
        elif self.path < 8:
            step = 8
        else:
            return position
        for i in range(move.start+step*self.sign,move.stop,step*self.sign):
            if position.board[i]:
                return position
        if move.start in self.castle_map:
            position.castleflag &= self.castle_map[move.start]
        position.board[move.start] = 0
        position.board[move.stop] = move.piece_id
        return position
            
    def knight_rules(self, position, move):
        if self.path in [0x1f,0x21,0xe,0x12]:
            position.board[move.start] = 0
            position.board[move.stop] = move.piece_id
            return position
        else:
            return position

    def bishop_rules(self, position, move):
        if self.path % 0x11 == 0:
            step = 0x11
        elif self.path % 0xf == 0:
            step = 0xf
        else:
            return position
        for i in range(move.start+step*self.sign,move.stop,step*self.sign):
            if position.board[i]:
                return position
        position.board[move.start] = 0
        position.board[move.stop] = move.piece_id
        return position

    def queen_rules(self, position, move):
        if self.path % 0x11 == 0 or self.path % 0xf == 0:
            return self.bishop_rules(position, move)
        elif self.path % 0x20 or self.path < 8:
            return self.rook_rules(position, move)
        else:
            return position
    
    def king_rules(self, position, move):
        if self.path in [1,0xf,0x10,0x11]:
            position[move.start] = 0
            position[move.stop] = move.piece_id
        elif self.path == 2 and move.start == 4 and position.castleflag&0x0100:
            # check collision
            pass
        elif self.path == 2 and move.start == 0x74 and position.castleflag&0x0001
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

    def takeback(self):
        self.position = self.history[-1]
        self.history.pop(-1)