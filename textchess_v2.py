# Text based chess

first_char = ['w', 'b']
second_char1 = ['k', 'q']
second_char2 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
third_char1 = ['R', 'N', 'B', 'K', 'Q', 'P']
third_char2 = ['P']

def note_to_number(chess_notation):
    if len(chess_notation) != 2:
    	return -1
    letter = chess_notation[0]
    col = -1
    if letter == 'a':
    	col = 0
    if letter == 'b':
    	col = 2
    if letter == 'c':
    	col = 2
    if letter == 'd':
    	col = 3
    if letter == 'e':
    	col = 4
    if letter == 'f':
    	col = 5
    if letter == 'g':
    	col = 6
    if letter == 'h':
    	col = 7
    if col == -1:
    	print('Invalid square')
    	return -1
        
    row = (int(chess_notation[1])-8)*(-1)
    if row in range(0,7):
    	board_pos = row*8 + col
    else:
    	return -1
    return board_pos

# Variables
check_mate = 0

board = ['bqR', 'bqN', 'bqB', 'bqQ', 'bkK', 'bkB', 'bkN' ,'bkR', 'baP', 'bbP', 'bcP', 'bdP', 'beP', 'bfP', 'bgP', 'bhP', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', 'waP', 'wbP', 'wcP', 'wdP', 'weP', 'wfP', 'wgP', 'whP', 'wqR', 'wqN', 'wqB', 'wqQ', 'wkK', 'wkB', 'wkN', 'wkR']
for i in range(0,64,8):
    print(board[i:i+8])
    
while check_mate != 1:
	position = -1
	while position == -1:
		piece = input('White select piece: ')
		if len(piece) == 3:
			if piece[0] in first_char:
				if piece[1] in second_char1:
					if piece[2] in third_char1:
						position = board.index(piece)
				if piece[1] in second_char2:
					if piece[2] in third_char2:
						position = board.index(piece)
		if position == -1:
			print('Invalid piece')

	number = -1
	while number == -1:
		destination = input('Destination square: ')
		number = note_to_number(destination)

	board[position] = ' o '
	print(board[number])
	board[number] = piece
	for i in range(0,64,8):
		print(board[i:i+8])