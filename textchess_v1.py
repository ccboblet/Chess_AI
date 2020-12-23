# Text based chess

# Variables
check_mate = 0

# Chess notation to numbers
a = 1
b = 2
c = 3
d = 4
e = 5
f = 6
g = 7
h = 8

# White major pieces starting positions
wqR = [1, 1]
wqN = [2, 1]
wqB = [3, 1]
wqQ = [4, 1]
wkK = [5, 1]
wkB = [6, 1]
wkN = [7, 1]
wkR = [8, 1]

# White pawns starting posistions
waP = [1, 2]
wbP = [2, 2]
wcP = [3, 2]
wdP = [4, 2]
weP = [5, 2]
wfP = [6, 2]
wgP = [7, 2]
whP = [8, 2]

# Black pawns starting positions
baP = [1, 7]
bbP = [2, 7]
bcP = [3, 7]
bdP = [4, 7]
beP = [5, 7]
bfP = [6, 7]
bgP = [7, 7]
bhP = [8, 7]

# Black major pieces starting posistions
bqR = [1, 8]
bqN = [2, 8]
bqB = [3, 8]
bqQ = [4, 8]
bkK = [5, 8]
bkB = [6, 8]
bkN = [7, 8]
bkR = [8, 8]

board = ['wqR', 'wqN', 'wqB', 'wqQ', 'wkK', 'wkB', 'wkN' ,'wkR', 'waP', 'wbP', 'wcP', 'wdP', 'weP', 'wfP', 'wgP', 'whP', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', ' o ', 'baP', 'bbP', 'bcP', 'bdP', 'beP', 'bfP', 'bgP', 'bhP', 'bqR', 'bqN', 'bqB', 'bqQ', 'bkK', 'bkB', 'bkN', 'bkR']
for i in range(1,64,8):
    print(board[i:i+7])
    
while check_mate != 1:
    piece = input('White select piece: ')
    destination = input('Destination square: ')
	