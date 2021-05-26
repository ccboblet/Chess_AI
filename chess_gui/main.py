from tkinter import mainloop
from gui_v2 import *

chess = Board()
position = Position()
chess.load_images('img/')
chess.make_pieces(position)
chess.init_bindings()

chess.root.mainloop()