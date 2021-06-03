from operator import pos
import numpy as np
from copy import copy

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

        self.king_castle = {}

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
        piece = position.board[move.start]
        dest = position.board[move.stop]
        if piece&8 ^ dest&8:
            self.path = move.start-move.stop if move.start>move.stop else move.stop-move.start
            self.sign = (move.start-move.stop)/self.path
            new = copy(position)
            new = self.rule_map[piece&7](new, move)
            if self.find_checks(new):
                # if a new enpassant has not been set this turn:
                # set the enpassant square outside of the board
                if position.enpassant == new.enpassant:
                    new.enpassant = 0xffff
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
        # Extract the position of a rook given the path and the king's id
        # Use that rook as the key to the castle_map dictionary
        # XOR that value to give a bitmap that you can and with the castleflag
        castle_id = (self.path-2)*7+self.piece_id-4
        flag = self.castle_map[castle_id]^0b1111

        if self.path in [1,0xf,0x10,0x11]:
            if move.start in self.castle_map:
                position.castleflag &= self.castle_map[move.start]
            position.board[move.start] = 0
            position.board[move.stop] = move.piece_id
        elif position.castleflag&flag:
            for i in range(move.start+self.sign,move.stop,self.sign):
                if position.board[i]:
                    return position
            position.board[move.start] = 0
            position.board[move.stop+self.sign] = 0
            position.board[move.stop] = move.piece_id
            position.board[move.stop-self.sign] = castle_id
            return position

    def pawn_rules(self, position, move):
        # Check up or down direction with color
        # Check forward moves to ensure no capture
        # Check for collisions on dash
        # Check for capture on diagonal moves
        # Check for en passant capture
        if self.sign > 0 ^ move.piece_id&8:
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