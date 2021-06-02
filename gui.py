from sys import path
from tkinter import *
from PIL import Image, ImageTk
from numpy import uint8, where
import os
import copy

# Define sizes and colors of pieces and squares
board_size = 600
square_size = int(board_size/8)
piece_size = int(board_size/10)
square_white = 'MediumPurple3'
square_black = 'LightPink3'
piece_white = 'color'
piece_black = 'color'
top = range(0,8)
bottom = range(56,64)
right = range(0,64,8)
left = range(7,64,8)
edge = list()
for i in top,bottom,right,left:
    for j in i:
        edge.append(j)

class Board:
    def __init__(self):
        # Create tkinter root and canvas
        self.root = Tk()
        self.root.title("Bobble Chess")
        self.root.iconbitmap('icon.ico')
        self.root.geometry('800x600')
        self.board = Canvas(self.root)
        self.board.pack(fill='both', expand=True)

        # Create squares with defined colors
        color = square_white
        for i in range(0,board_size,square_size):
            if color == square_white:
                color = square_black
            else:
                color = square_white
            for j in range(0,board_size,square_size):
                self.board.create_rectangle(i,j,i+square_size,j+square_size,fill=color)
                if color == square_white:
                    color = square_black
                else:
                    color = square_white

        # Initialize variable used in select, hover and teleport
        self.moving = -1
        self.source = 0
        self.piece_id = range(0,32)
        self.history = list()

        self.position = Position()

    def load_images(self, folder):
        # Tkinter needs images to be global
        global renders
        renders = list()

        # Order piece images are stored in folder
        order = [0,1,2,3,4,2,1,0,5,5,5,5,5,5,5,5,11,11,11,11,11,11,11,11,6,7,8,9,10,8,7,6]
        images = os.listdir(folder)
        for i in order:
            image = Image.open(folder + images[i])
            image = image.resize((piece_size,piece_size))
            renders.append(ImageTk.PhotoImage(image))

    def make_promote_pieces(self):
        global renders
        order = [0,1,2,3,24,25,26,27]
        self.promotion_dict = {}
        center = self.move.stop
        board_center = self.translate_xy([center])
        color = ((self.move.piece_id // 8)-1)*4 # 1 is black 2 is white
        for i in range(0,4):
            offset = square_size*i-square_size*1.5
            self.promotion_dict[self.board.create_image(board_center[0][0]-offset,board_center[0][1],anchor=CENTER,image=renders[order[i+color]])] = order[i+color]

    def make_pieces(self, position):
        # Tkinter needs image variables to be global
        global renders

        self.piece_dict = {}
        self.position = position
        
        xy_position = self.translate_xy(self.position.pieces)
        for i in range(0,32):
            if i!=4 and i!=28:
                if self.position.pieces[i] == self.position.pieces[4] or self.position.pieces[i] == self.position.pieces[28]:
                    self.piece_dict[-i] = -1
                    continue
            self.piece_dict[self.board.create_image(xy_position[i][0],xy_position[i][1],anchor=CENTER,image=renders[self.piece_id[i]])] = self.piece_id[i]
        return True

    def clear_board(self):
        self.piece_id = list()
        all = self.board.find_all()
        for i in self.piece_dict:
            self.piece_id.append(self.piece_dict[i])
            if i in all:
                self.board.delete(i)

    def select_piece(self):
        # Create button-1 event to select a piece
        def select(e):
            x = e.x
            y = e.y
            objects = self.board.find_overlapping(x-5,y-5,x+5,y+5)
            for piece in objects:
                if piece in self.piece_dict:
                    if (self.piece_dict[piece] < 16) ^ (self.position.move == 0):
                        break
                    self.moving = piece
                    self.source = self.board.coords(self.moving)

        self.board.bind('<Button-1>', select)

    def hover_piece(self):
        # Make selected piece follow the mouse
        def hover(e):
            if self.moving in self.board.find_all():
                location = self.board.coords(self.moving)
                self.board.move(self.moving, e.x-location[0],e.y-location[1])

        self.board.bind('<B1-Motion>', hover)

    def teleport_piece(self):
        def teleport(e):
            if self.moving in self.board.find_all():
                # Translate 600x600 board coordinates to 0-63 position coordinates
                start = self.board_to_coord(self.source)
                stop = self.board_to_coord([e.x,e.y])

                # Test if move is legal
                piece_id = self.piece_dict[self.moving]
                self.move = Move(start, stop, piece_id)
                if self.check_move():
                    if self.find_checks():
                        self.position.move ^= 1
                    else:
                        self.takeback()

                self.clear_board()
                self.make_pieces(self.position)
                self.moving=-1

        self.board.bind('<ButtonRelease-1>', teleport)

    def promotion(self):
        # detect which piece was picked for promotion
        # the piece_id in self.move is the pawn that was promoted
        # change the pawn's piece_id in the dict to that piece_id
        self.make_promote_pieces()
        def promote(e):
            x = e.x
            y = e.y
            objects = self.board.find_overlapping(x-5,y-5,x+5,y+5)
            for piece in objects:
                if piece in self.promotion_dict:
                    # change piece id of the image to piece_id of selected image
                    # find image id of promoted piece?
                    for i in self.piece_dict:
                        if self.piece_dict[i] == self.move.piece_id:
                            image_id = i
                            break
                    self.piece_dict[image_id] = self.promotion_dict[piece]
                    for i in self.promotion_dict:
                        self.board.delete(i)
                    self.clear_board()
                    self.make_pieces(self.position)
                    self.init_bindings()
                    

        self.board.bind('<Button-1>', promote)

    def init_bindings(self):
        self.select_piece()
        self.hover_piece()
        self.teleport_piece()

    # Board coordinates to 0-63
    def board_to_coord(self, board):
        x = int(board[0]/square_size)
        y = int(board[1]/square_size)
        return x+(y*8)

    # 0-63 to 0-8,0-8 coordinates
    # go straight to board coords
    def translate_xy(self, position):
        xy = []
        for i in position:
            row = i&7
            col = i>>3
            xy.append([row*square_size+square_size/2,col*square_size+square_size/2])
        return xy

    def check_move(self):
        if self.move.start == self.move.stop:
            return False
        self.path = int(self.move.stop)-int(self.move.start)
        self.sign = int(self.path/abs(self.path))
        if self.move.stop in self.position.pieces:
            for i in range(31):
                if self.position.pieces[i] == self.move.stop:
                    if (self.move.piece_id in range(0,16)) ^ (i in range(17,32)):
                        # illegal capture
                        return False
        
        self.save_position()
        if self.move.piece_id in [0,7,24,31]:
            if not self.rook_rules():
                return False
        elif self.move.piece_id in [1,6,25,30]:
            if not self.knight_rules():
                return False
        elif self.move.piece_id in [2,5,26,29]:
            if not self.bishop_rules():
                return False
        elif self.move.piece_id in [3,27]:
            if not self.queen_rules():
                return False
        elif self.move.piece_id in [4,28]:
            if not self.king_rules():
                return False
        elif self.move.piece_id in range(8,24):
            if not self.pawn_rules():
                return False
        else:
            return False
        return True

    def update_position(self):
        if self.position.enpassant != self.move.stop:
            self.position.enpassant = uint8(0)
        if self.move.stop in self.position.pieces:
            captured = where(self.position.pieces == self.move.stop)
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
            if self.sign<0 and self.move.start in right:
                return False
            if self.sign>0 and self.move.start in left:
                return False
            for i in range(self.move.start+self.sign,self.move.stop,self.sign):
                if i in right or i in left:
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
        if self.move.start in right and self.move.stop in left:
            return False
        if self.move.start in left and self.move.stop in right:
            return False
        if self.move.start in right and self.move.stop in left:
            return False
        if abs(self.path) in [15,17,10,6]:
            self.update_position()
            return True
        else:
            return False

    def bishop_rules(self):
        if abs(self.path) % 7 == 0:
            if self.sign<0 and self.move.stop in right:
                return False
            elif self.sign>0 and self.move.stop in left:
                return False
            for i in range(self.move.start+7*self.sign,self.move.stop,7*self.sign):
                if i in right or i in left:
                    return False
                if i in self.position.pieces:
                    return False
        elif abs(self.path) % 9 == 0:
            if self.sign>0 and self.move.stop in right:
                return False
            elif self.sign<0 and self.move.stop in left:
                return False
            for i in range(self.move.start+9*self.sign,self.move.stop,9*self.sign):
                if i in right or i in left:
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
            if self.move.start in right and self.move.stop in left:
                return False
            if self.move.start in left and self.move.stop in right:
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
        if self.move.start in right and self.move.stop in left:
            return False
        if self.move.start in left and self.move.stop in right:
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
        self.pieces = uint8([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63])
        # 2 sets of 2 for each castle 
        # 1 = able to castle
        # if the king move then both are set to 0
        self.castleflag = 0b1111
        # When a pawn double moves set the en passant square
        self.enpassant = uint8(0)
        # Move 1 = white, 0 = black
        self.move = 0b1

    def import_position(self, position):
        self.pieces = copy.copy(position.pieces)
        self.castleflag = position.castleflag
        self.enpassant = position.enpassant
        self.move = position.move