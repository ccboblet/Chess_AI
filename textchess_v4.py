import textchess_methods_v1

def main():
    board = textchess_methods_v1.init_board()
    while True:
        textchess_methods_v1.print_board(board)
        
        something = input('What color would you like to play? ')

        if something == 'test':
            legal_moves = []
            for i in range(0,64):
                legal_moves.append(i)
            piece = input('Select a piece: ')
            for move in range(0,64):
                legal_moves[move] = ' o '
                if 'P' in piece:
                    legal = textchess_methods_v1.pawn_move(board, move, piece)
                else:
                    for square in range(0,64):
                        if 'P' in board[square]:
                            board[square] = ' o '
                if 'R' in piece:
                    legal = textchess_methods_v1.rook_move(board, move, piece)
                if 'N' in piece:
                    legal = textchess_methods_v1.knight_move(board, move, piece)
                if 'B' in piece:
                    legal = textchess_methods_v1.bishop_move(board, move, piece)
                if 'Q' in piece:
                    legal = textchess_methods_v1.queen_move(board, move, piece)
                if 'K' in piece:
                    legal = textchess_methods_v1.king_move(board, move, piece)
                if legal is True:
                    legal_moves[move] = ' M '
            else:
                textchess_methods_v1.print_board(legal_moves)



main()