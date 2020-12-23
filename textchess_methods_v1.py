

# Initializes the board for a new game and returns the new board
def init_board():
	board = ['wqR', 'wqN', 'wqB', 'wqQ', 'wkK', 'wkB', 'wkN' ,'wkR', 'waP', 'wbP', 'wcP', 'wdP', 'weP', 'wfP', 'wgP', 'whP', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', 'baP', 'bbP', 'bcP', 'bdP', 'beP', 'bfP', 'bgP', 'bhP', 'bqR', 'bqN', 'bqB', 'bqQ', 'bkK', 'bkB', 'bkN', 'bkR']
	return board

# Prints the board
def print_board(board):
	col_letters = [' a ', ' b ', ' c ', ' d ', ' e ', ' f ', ' g ', ' h ']
	row_numbers = [' 1 ', ' 2 ', ' 3 ', ' 4 ', ' 5 ', ' 6 ', ' 7 ', ' 8 ']
	for i in range(0,8):
		print(row_numbers[7-i], ' ', board[56-i*8:64-i*8])
	else:
		print('\n     ', col_letters, '\n')

# Asks the user to select a piece to move
# Input - board to check if the piece has not been taken
def get_piece(board):
	while True:
		piece = input('Select a piece: ')
		if piece in board:
			return True
		else:
			print('Invalid entry')

# Asks the user for the destination of their selected piece
def get_move(board, piece):
	col_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
	row_numbers = ['1', '2', '3', '4', '5', '6', '7', '8']
	while True:

		# Get the move from the user
		move = input('Select a destination square: ')

		# Check the input has correct format
		if len(move) == 2 and move[0] in col_letters and move[1] in row_numbers:

			# Translate input into list index
			col = col_letters.index(move[0])
			row = int(move[1])-1
			square = row*8 + col

			# Check move for trying to capture own piece or staying still
			if board.index(piece) != square:
				# Check for trying to capture own piece
				if 'w' in piece and 'w' in board[square]:
					print('Invalid entry')
					continue
				if 'b' in piece and 'b' in board[square]:
					print('Invalid entry')
					continue
				return square
		print('Invalid entry')

# Checks if the selected move is legal
# This will be the most complex
# Do I just want to calculate all possible moves and check that list? It would make future applications easier.
# Inputs - board, destination, piece
# Return - True for a legal move, False for a illegal move
def rook_move(board, move, piece):
	position = board.index(piece)
	if move<position:
		step = -1
	else:
		step = 1

	# Check for a move along the file
	difference = abs(position-move)
	if difference in range(0,64,8):

		# Check for collision along the file
		for square in range(position, move, 8*step):
			# Have to pass the first square as it will contain the piece that is moving
			if board[square] != ' o ' and board[square] != piece:
				return False
		return True

	# Check each row for the position and move
	for i in range(0,64,8):
		if move in range(i,i+8) and position in range(i,i+8):

			# Check for collision
			for square in range(position, move, step):
				if board[square] != ' o ' and board[square] != piece:
					return False
			return True
	return False

def bishop_move(board, move, piece):
	position = board.index(piece)

	# Detects move along the positive diagonal
	difference = move-position
	if abs(difference) in range(0,64,9):
		if move<position:
			step = -9
		else:
			step = 9
	elif abs(difference) in range(0,64,7):
		if move<position:
			step = -7
		else:
			step = 7
	else:
		return False
	# Add a statement to return false if its not on a diagonal at all

	# Find if the piece is going left or right and select a side for collision detection
	if step in [9, -7]:
		side = range(7,64,8)
	elif step in [-9, 7]:
		side = range(0,64,8)
	else:
		return False
	
	for square in range(position, move, step):
		if square in side or (board[square] != ' o ' and board[square] != piece):
			return False
	return True

def knight_move(board, move, piece):
	position = board.index(piece)
	difference = move - position

	# There are only 8 possible knight moves
	# The difference comparison ensures there are no problems with the ranks
	if abs(difference) not in [17, 15, 10, 6]:
		return False
	# Moves to the left from the a file are illegal
	if position in range(0,64,8):
		if difference in [15, 6, -10, -17]:
			return False
	 # Moves 2 to the left from the b file are illegal
	if position in range(1,64,8):
		if difference in [6, -10]:
			return False

	# Moves 2 to the right from the g file are illegal
	if position in range(6,64,8):
		if difference in [10,-6]:
			return False

	# Moves to the right from the h file are illegal
	if position in range(7,64,8):
		if difference in [17, 10, -6, -15]:
			return False
	return True

def queen_move(board, move, piece):
	if rook_move(board, move, piece):
		return True
	elif bishop_move(board, move, piece):
		return True
	else:
		return False

def king_move(board, move, piece):
	position = board.index(piece)
	difference = abs(move - position)
	if difference in [7, 9]:
		if bishop_move(board, move, piece):
			return True
	elif difference in [1, 8]:
		if rook_move(board, move, piece):
			return True
	elif difference == 2:
		# implement castling
		return False
	else:
		return False

def pawn_move(board, move, piece):

	# Calculate current position and move distance
	position = board.index(piece)
	difference = move - position

	# Set color specific variables
	if 'w' in piece:
		direction = 1
		start = range(8,16)
		promotion = range(56,64)
	else:
		direction = -1
		start = range(48,56)
		promotion = range(0,8)
	
	if difference == 8*direction and board[move] == ' o ':
		if move in promotion:
			promotion = input('Choose promotion: ')
			if len(promotion) == 1 and promotion in ['R', 'N', 'B', 'Q']:
				return promotion
			return True
		return True
	elif difference == 16*direction and board[move] == ' o ' and position in start:
		return True
	elif difference in [7*direction, 9*direction] and board[move] != ' o ':
		# check for en passant
		return True
	else:
		return False


def find_check():
	something = 1
	return something

# Moves the piece to the new square
def move_piece():
	something = 1
	return something