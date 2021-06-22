from tkinter import mainloop
import gui
import board_reps as br


chess = gui.Board()
chess.make_squares()
position = br.Board_0x88()
chess.load_images('img/')
pp = br.B88_to_Print(position)
chess.make_pieces(pp)
chess.select_piece()
chess.hover_piece()
chess.teleport_piece()

chess.root.mainloop()