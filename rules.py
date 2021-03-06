from operator import pos
import numpy as np
from copy import deepcopy
import board_reps as br

# Make a function to find collisions
# Disable castle through check

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
    def make_move(self, position, move):
        new = self.check_move(position, move)
        if new.board[move.start] == 0:
            if self.find_checks(new):
                return new
        return position

    def check_move(self, position, move):
        piece = position.board[move.start]
        dest = position.board[move.stop]
        if piece != move.piece_id:
            return position
        if piece&8 ^ dest&8 or dest == 0:
            self.path = move.start-move.stop if move.start>move.stop else move.stop-move.start
            self.sign = (move.stop-move.start)//self.path
            new = deepcopy(position)
            new = self.rule_map[piece&7](new, move)
            #if self.find_checks(new):
            # if a new enpassant has not been set this turn:
            # set the enpassant square outside of the board
            if position.enpassant == new.enpassant:
                new.enpassant = 0xff
            new.turn ^= 1
            return new
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
        elif self.path % 0x10 == 0 or self.path < 8:
            return self.rook_rules(position, move)
        else:
            return position
    
    def king_rules(self, position, move):
        # Extract the position of a rook given the path and the king's id
        # Use that rook as the key to the castle_map dictionary
        # XOR that value to give a bitmap that you can and with the castleflag

        if self.path in [1,0xf,0x10,0x11]:
            if move.start in self.castle_map:
                position.castleflag &= self.castle_map[move.start]
            position.board[move.start] = 0
            position.board[move.stop] = move.piece_id
        elif self.path == 0x02:
            rook_position = move.start+3 if self.sign == 1 else move.start-4
            flag = self.castle_map[rook_position]^0b1111
            if flag&position.castleflag:
                for i in range(move.start+self.sign,rook_position,self.sign):
                    if position.board[i]:
                        return position
                position.board[move.start] = 0
                position.board[move.stop] = move.piece_id
                position.board[rook_position] = 0
                position.board[move.stop-self.sign] = move.piece_id-4
        return position

    def pawn_rules(self, position, move):
        # Check up or down direction with color
        # Check forward moves to ensure no capture
        # Check for collisions on dash
        # Check for capture on diagonal moves
        # Check for en passant capture
        if (self.sign<0) ^ (move.piece_id>>3):
            return position
        if self.path % 0x10 == 0:
            if position.board[move.stop]:
                return position
            elif self.path == 0x20:
                if position.board[move.start+0x10*self.sign]:
                    return position
                else:
                    position.board[move.start] = 0
                    position.board[move.stop] = move.piece_id
                    position.enpassant = move.stop-0x10*self.sign
            elif self.path == 0x10:
                position.board[move.start] = 0
                position.board[move.stop]  = move.piece_id
        elif self.path in [0x11,0xf]:
            if position.board[move.stop]:
                position.board[move.start] = 0
                position.board[move.stop] = move.piece_id
            elif move.stop == position.enpassant:
                position.board[move.start] = 0
                position.board[move.stop-0x10*self.sign] = 0
                position.board[move.stop] = move.piece_id
        if move.stop >= 0x70 or move.stop <=0x07:
            position.promotion = move.stop
        return position

    def find_checks(self, position):
        enemy = dict()
        king_enemy = [5,8] if position.turn == 1 else [13,0]
        for i, j in enumerate(position.board):
            if j == king_enemy[0]:
                index = i
            elif j&8 == king_enemy[1] and j != 0:
                enemy[i] = j
        for i in enemy:
            move = br.Move(i,index,enemy[i])
            test = self.check_move(position, move)
            if test.board[index] == enemy[i]:
                #test.board[index] = king_enemy[0]
                #test.board[i] = enemy[i]
                return False
        return True

