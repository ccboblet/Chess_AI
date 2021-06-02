from tkinter import mainloop
import gui
import rules

chess = gui.Board()
position = gui.Position()
chess.load_images('img/')
chess.make_pieces(position)
chess.init_bindings()

chess.root.mainloop()