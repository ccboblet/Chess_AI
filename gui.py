from sys import path
from tkinter import *
from PIL import Image, ImageTk
from numpy import uint8, where
import os
import copy
from board_reps import Piece_Major_32 as Position

# This class creates a board gui that is capable of detecting moves
# It calls the rules class when a move is detected to recieve the updated position

# Eventual features - clock, board color, piece color/style choice, ai difficulty/style, etc

# Define sizes and colors of pieces and squares

# To do list move rules out of gui
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
        self.root.iconbitmap('img_tk/icon.ico')
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

class Move:
    def __init__(self, start, stop, piece_id):
        self.start = start
        self.stop = stop
        self.piece_id = piece_id