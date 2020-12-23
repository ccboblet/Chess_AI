# Text based chess

# Defines
first_char = ['w', 'b']
second_char1 = ['k', 'q']
col_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
third_char1 = ['R', 'N', 'B', 'K', 'Q', 'P']
third_char2 = ['P']
row_numbers = ['1', '2', '3', '4', '5', '6', '7', '8']
board = ['wqR', 'wqN', 'wqB', 'wqQ', 'wkK', 'wkB', 'wkN' ,'wkR', 'waP', 'wbP', 'wcP', 'wdP', 'weP', 'wfP', 'wgP', 'whP', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', 'baP', 'bbP', 'bcP', 'bdP', 'beP', 'bfP', 'bgP', 'bhP', 'bqR', 'bqN', 'bqB', 'bqQ', 'bkK', 'bkB', 'bkN', 'bkR']

# Methods

def init_board():
	board = ['wqR', 'wqN', 'wqB', 'wqQ', 'wkK', 'wkB', 'wkN' ,'wkR', 'waP', 'wbP', 'wcP', 'wdP', 'weP', 'wfP', 'wgP', 'whP', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', 'baP', 'bbP', 'bcP', 'bdP', 'beP', 'bfP', 'bgP', 'bhP', 'bqR', 'bqN', 'bqB', 'bqQ', 'bkK', 'bkB', 'bkN', 'bkR']
	for i in range(0,64,8):
		print(board[56-i:64-i])

def print_board():
	for i in range(0,64,8):
		print(board[56-i:64-i])

def note_to_number(chess_notation):

	# Check format of the string
	if len(chess_notation) != 2:
		return -1
	if chess_notation[0] not in col_letters:
		return -1
	if chess_notation[1] not in row_numbers:
		return -1

	# Translate to list index
	col = col_letters.index(chess_notation[0])
	row = (int(chess_notation[1]))-1
	board_pos = row*8 + col
	return board_pos

def main():
	# Variables
	check_mate = 0

	# Main
	init_board()

	# Main loop until game over
	while check_mate != 1:

		# Get move

		# Select piece
		position = -1
		while position == -1:
			piece = input('White select piece: ')
			if len(piece) == 3:
				if piece[0] in first_char:
					if piece[1] in second_char1:
						if piece[2] in third_char1:
							position = board.index(piece)
					if piece[1] in col_letters:
						if piece[2] in third_char2:
							position = board.index(piece)
			if position == -1:
				print('Invalid piece')

		# Select destination square
		number = -1
		while number == -1:
			destination = input('Destination square: ')
			number = note_to_number(destination)
			if number == -1:
				print('Invalid square')

		# Move piece
		board[position] = ' o '
		board[number] = piece
		print_board()



