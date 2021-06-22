import tkinter as tk
from PIL import Image, ImageTk
import os
import board_reps as br
import rules

'''
Known issues
Weird math in make_pieces() to get board coordinates
Magic number 6 in selected()
'''

# This class creates a board gui that is capable of detecting moves
# It calls the rules class when a move is detected to recieve the updated position

# Eventual features - clock, board color, piece color/style choice, ai difficulty/style, etc

# Define sizes and colors of pieces and squares

# To do list move rules out of gui
board_size = 600
square_size = int(board_size/8)
piece_size = int(board_size/10)

# piece_dict - image_id: piece_id

class Board:
    def __init__(self):
        # Create tkinter root and canvas
        self.root = tk.Tk()
        self.root.title("Bobble Chess")
        self.root.iconbitmap('img_tk/icon.ico')
        self.root.geometry('800x600')
        self.board = tk.Canvas(self.root)
        self.board.pack(fill='both', expand=True)

        # Initialize variable used in select, hover and teleport
        self.moving = -1
        self.source = -1
        self.history = list()

        self.position = br.Board_0x88()
        self.rules = rules.Rules()

    def make_squares(self,square_color=['MediumPurple3','LightPink3']):
        white = square_color[0]
        black = square_color[1]
        # Create squares with defined colors
        color = white
        for i in range(0,board_size,square_size):
            if color == white:
                color = black
            else:
                color = white
            for j in range(0,board_size,square_size):
                self.board.create_rectangle(i,j,i+square_size,j+square_size,fill=color)
                if color == white:
                    color = black
                else:
                    color = white

    def load_images(self, folder):
        # Tkinter needs images to be global
        global renders
        renders = list()

        # Order piece images are stored in folder
        flname = os.listdir(folder)
        for i in flname:
            image = Image.open(folder + i)
            image = image.resize((piece_size,piece_size))
            renders.append(ImageTk.PhotoImage(image))

    # Given any position print the pieces to the board. The pieces need to already be loaded.
    def make_pieces(self, position):
        # Tkinter needs image variables to be global
        global renders

        # Create a dict to connect tkinter image_id with the piece_id
        # Position is a dict in format square(0-63): piece_id(0-11)
        self.piece_dict = {}
        
        for i in position:
            m = (i>>3)*square_size+square_size/2
            n = (i&7)*square_size+square_size/2
            self.piece_dict[self.board.create_image(n,m,anchor=tk.CENTER,image=renders[position[i]])] = position[i]+1 if position[i] <= 5 else position[i]+3

    def clear_board(self):
        all = self.board.find_all()
        for i in self.piece_dict:
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
                    if (self.piece_dict[piece] <= 6) ^ (self.position.turn == 0):
                        break
                    self.moving = piece
                    self.source = self.board.coords(self.moving)

        self.board.bind('<Button-1>', select)

    def hover_piece(self):
        # Make selected piece follow the mouse
        def hover(e):
            x = e.x
            y = e.y
            if self.moving >= 0:
                location = self.board.coords(self.moving)
                self.board.move(self.moving, x-location[0],y-location[1])

        self.board.bind('<B1-Motion>', hover)

    def teleport_piece(self):
        def teleport(e):
            if self.moving >= 0:
                x = e.x
                y = e.y
                # Translate 600x600 board coordinates to 0-63 position coordinates
                start = self.board_to_coord(self.source)
                stop = self.board_to_coord([x,y])
                if x>board_size or y>board_size:
                    stop = start
                # Test if move is legal
                piece_id = self.piece_dict[self.moving]

                move = Move(start, stop, piece_id)
                self.position = self.rules.make_move(self.position,move)

                self.clear_board()
                self.make_pieces(br.B88_to_Print(self.position))
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
        return x+(y*0x10)

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