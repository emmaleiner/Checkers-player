import operator
import random



def display(board):
    for line in board:
        print(line)

class Jump(object):
    def __init__(self, row, col, board, children=None):
        self.row = row
        self.col = col
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)
        self.board = board # state of the board after doing that move
    def __repr__(self):
        return "({}, {})".format(self.row, self.col)
    def add_child(self, node):
        assert isinstance(node, Jump)
        self.children.append(node)
    def get_paths(self):
        children = self.children.copy()
        paths = [[self, child] for child in self.children]
        explored_paths = []
        while len(children) > 0:
            enum_paths = paths.copy()
            for path in enum_paths:
                if path not in explored_paths:
                    children.remove(path[-1])
                    if len(path[-1].children) != 0:
                        paths.remove(path)
                    else:
                        explored_paths.append(path) # if we're a the end of the path, add it to the explored paths list
                    for child in path[-1].children:
                        paths.append(path + [child])
                        children.append(child)
        return paths


def replace_str(idx, value, string):
    return string[:idx] + value + string[idx+1:]


def update_board(board, move, color):
    N = len(board)
    updated_board = board.copy()
    current_idx = 0
    next_idx = 1

    while next_idx < len(move):
        current = move[current_idx]
        row = current[0]
        col = current[1]

        next_ = move[next_idx]
        next_row = next_[0]
        next_col = next_[1]

        player = color

        if updated_board[row][col] == updated_board[row][col].upper():
            player = color.upper() # if it is a king

        # if reaches the edge of the board, become king
        if color == 'b':
            if next_[0] == N-1:
                player = color.upper()
        if color == 'w':
            if next_[0] == 0:
                player = color.upper()

        # non-capturing move
        if abs(row - next_row) == 1 and abs(col - next_col) == 1:
            updated_board[row] = replace_str(col, '_', updated_board[row])
            updated_board[next_row] = replace_str(next_col, player, updated_board[next_row])

        # capturing move
        if abs(row - next_row) == 2 and abs(col - next_col) == 2:
            middle_row = int((row + next_row) / 2)
            middle_col = int((col + next_col) / 2)

            updated_board[row] = replace_str(col, '_', updated_board[row])
            updated_board[middle_row] = replace_str(middle_col, '_', updated_board[middle_row])
            updated_board[next_row] = replace_str(next_col, player, updated_board[next_row])

        current_idx += 1
        next_idx += 1

    return updated_board


def capturing_moves(board, row, col, color, is_king):
    N = len(board)
    moves = []

    # Black moves downwards, White moves upwards

    if color == 'b':

        # If on the edge, you become a king
        if row == N-1:
            is_king = True
            board[row] = replace_str(col, board[row][col].upper(), board[row]) # update the board

        # player is the character that will appear on the board
        if is_king:
            player = color.upper()

            # a king can move in the opposite direction as well
            if row > 1:
                if col < N-2:
                    if board[row-1][col+1].lower() == 'w' and board[row-2][col+2] == '_':

                        # update the board
                        move = [(row, col), (row-2, col+2)]
                        updated_board = update_board(board, move, color)

                        # this new position becomes a possible move
                        moves.append(Jump(row-2, col+2, updated_board))
                if col > 1:
                    if board[row-1][col-1].lower() == 'w' and board[row-2][col-2] == '_':
                        move = [(row, col), (row-2, col-2)]
                        updated_board = update_board(board, move, color)
                        moves.append(Jump(row-2, col-2, updated_board))

        else:
            player = color

        # Jumps for "everybody"
        # allow moves only if not on the edges
        if row < N-2:
            if col < N-2:
                if board[row+1][col+1].lower() == 'w' and board[row+2][col+2] == '_':
                    move = [(row, col), (row+2, col+2)]
                    updated_board = update_board(board, move, color)
                    moves.append(Jump(row+2, col+2, updated_board))
            if col > 1:
                if board[row+1][col-1].lower() == 'w' and board[row+2][col-2] == '_':
                    move = [(row, col), (row+2, col-2)]
                    updated_board = update_board(board, move, color)
                    moves.append(Jump(row+2, col-2, updated_board))


    # basically the same, but for whites
    if color == 'w':

        if row == 0:
            is_king = True
            board[row] = replace_str(col, board[row][col].upper(), board[row])

        if is_king:
            player = color.upper()

            if row < N-2:
                if col > 1:
                    if board[row+1][col-1].lower() == 'b' and board[row+2][col-2] == '_':
                        move = [(row, col), (row+2, col-2)]
                        updated_board = update_board(board, move, color)
                        moves.append(Jump(row+2, col-2, updated_board))
                if col < N-2:
                    if board[row+1][col+1].lower() == 'b' and board[row+2][col+2] == '_':
                        move = [(row, col), (row+2, col+2)]
                        updated_board = update_board(board, move, color)
                        moves.append(Jump(row+2, col+2, updated_board))

        else:
            player = color

        if row > 1:
            if col > 1:
                if board[row-1][col-1].lower() == 'b' and board[row-2][col-2] == '_':
                    move = [(row, col), (row-2, col-2)]
                    updated_board = update_board(board, move, color)
                    moves.append(Jump(row-2, col-2, updated_board))
            if col < N-2:
                if board[row-1][col+1].lower() == 'b' and board[row-2][col+2] == '_':
                    move = [(row, col), (row-2, col+2)]
                    updated_board = update_board(board, move, color)
                    moves.append(Jump(row-2, col+2, updated_board))

    return moves, is_king


def non_capturing_moves(board, row, col, color, is_king):
    N = len(board)
    moves = []

    # non-capturing moves are similar, but take only one step each time

    if color == 'b':
        if row == N-1:
            is_king = True
            board[row] = replace_str(col, board[row][col].upper(), board[row])

        if is_king:
            player = color.upper()

            if row > 0:
                if col < N-1:
                    if board[row-1][col+1] == '_':
                        move = [(row, col), (row-1, col+1)]
                        updated_board = update_board(board, move, color)
                        moves.append(Jump(row-1, col+1, updated_board))
                        
                if col > 0:
                    if board[row-1][col-1] == '_':
                        move = [(row, col), (row-1, col-1)]
                        updated_board = update_board(board, move, color)
                        moves.append(Jump(row-1, col-1, updated_board))

        else:
            player = color

        if row < N-1:
            if col < N-1:
                if board[row+1][col+1] == '_':
                    move = [(row, col), (row+1, col+1)]
                    updated_board = update_board(board, move, color)
                    moves.append(Jump(row+1, col+1, updated_board))
            if col > 0:
                if board[row+1][col-1] == '_':
                    move = [(row, col), (row+1, col-1)]
                    updated_board = update_board(board, move, color)
                    moves.append(Jump(row+1, col-1, updated_board))
                    
    if color == 'w':
        if row == 0:
            is_king = True
            board[row] = replace_str(col, board[row][col].upper(), board[row])
            
        if is_king:
            player = color.upper()

            if row < N-1:
                if col > 0:
                    if board[row+1][col-1] == '_':
                        move = [(row, col), (row+1, col-1)]
                        updated_board = update_board(board, move, color)
                        moves.append(Jump(row+1, col-1, updated_board))
                if col < N-1:
                    if board[row+1][col+1] == '_':
                        move = [(row, col), (row+1, col+1)]
                        updated_board = update_board(board, move, color)
                        moves.append(Jump(row+1, col+1, updated_board))

        else:
            player = color

        if row > 0:
            if col > 0:
                if board[row-1][col-1] == '_':
                    move = [(row, col), (row-1, col-1)]
                    updated_board = update_board(board, move, color)
                    moves.append(Jump(row-1, col-1, updated_board))
            if col < N-1:
                if board[row-1][col+1] == '_':
                    move = [(row, col), (row-1, col+1)]
                    updated_board = update_board(board, move, color)
                    moves.append(Jump(row-1, col+1, updated_board))

    return moves, is_king


# returns the allowed moves for a certain disk or king
def allowed_move_from_position(board, row, col):
    moves_dict = {'capturing': [], 'non-capturing': []}
    color = board[row][col].lower()
    is_king = board[row][col] != color # True if upper case, False if lower case

    # Explore possible capturing moves
    capturing, is_king = capturing_moves(board, row, col, color, is_king)
    # if no capturing moves available, make a non-capturing move and exit
    if len(capturing) == 0:
        non_capturing, is_king = non_capturing_moves(board, row, col, color, is_king)
        moves = []
        for move in non_capturing:
            moves.append([Jump(row, col, board), move])
        moves_dict['non-capturing'] += moves
        return moves_dict

    else:
        capturing_moves_tree = Jump(row, col, board, capturing)

        # explore possible moves until the disk (or king) has to stop
        while len(capturing) > 0:
            # the current move is not a move because the disk can still move
            for move in capturing.copy():
                # remove current move from the list and add the "new move"
                capturing.remove(move)
                children, is_king = capturing_moves(move.board, move.row, move.col, color, is_king)
                for child in children:
                    move.add_child(child)
                capturing += children

        # reconstruct all the paths as lists of positions
        moves = capturing_moves_tree.get_paths()
        moves_dict['capturing'] += moves
        return moves_dict


def allowed_moves(board, color):
    """
        This is the first function you need to implement.

        Arguments:
        - board: The content of the board, represented as a list of strings.
                 The length of strings are the same as the length of the list,
                 which represents a 8x8 checkers board.
                 Each string is a row, from the top row (the black side) to the
                 bottom row (white side). The string are made of five possible
                 characters:
                 - '_' : an empty square
                 - 'b' : a square with a black disc
                 - 'B' : a square with a black king
                 - 'w' : a square with a white disc
                 - 'W' : a square with a white king
                 At the beginning of the game:
                 - the top left square of a board is always empty
                 - the square on it right always contains a black disc
        - color: the next player's color. It can be either 'b' for black or 'w'
                 for white.

        Return value:
        It must return a list of all the valid moves. Please refer to the
        README for a description of what are valid moves. A move is a list of
        all the squares visited by a disc or a king, from its initial position
        to its final position. The coordinates of the square must be specified
        using (row, column), with both 'row' and 'column' starting from 0 at
        the top left corner of the board (black side).

        Example:
        >> board = [
            '________',
            '__b_____',
            '_w_w____',
            '________',
            '_w______',
            '_____b__',
            '____w___',
            '___w____'
        ]

        The top-most black disc can chain two jumps and eat both left white
        discs or jump only over the right white disc. The other black disc
        cannot move because it does produces any capturing move.

        The output must thus be:
        >> allowed_moves(board, 'b')
        [
            [(1, 2), (3, 0), (5, 2)],
            [(1, 2), (3, 4)]
        ]
    """

    # If one player has won, no more moves are possible
    moves_dict = {'capturing': [], 'non-capturing': []}
    N = len(board)
    for row in range(N):
        for col in range(N):
            if board[row][col].lower() == color:
                moves = allowed_move_from_position(board, row, col)
                moves_dict['capturing'] += moves['capturing']
                moves_dict['non-capturing'] += moves['non-capturing']
    if len(moves_dict['capturing']) == 0:
        return [[(move.row, move.col) for move in path] for path in moves_dict['non-capturing']]
    else:
        return [[(move.row, move.col) for move in path] for path in moves_dict['capturing']]


###############################################
###############################################
##########                           ##########
##########     MINIMAX ALGORITHM     ##########
##########                           ##########
###############################################
###############################################


def next_color(color):
	if color == 'w':
		return 'b'
	elif color == 'b':
		return 'w'


def score(board, color):
	# Black is "max", White is "min"
	# Returns the difference of number of black and white disks
	# A king is equivalent to 2 disks
    white = 0
    black = 0

    for row in board:
    	for value in row:
    		if value == "w":
    			white += 1
    		elif value == "W":
    			white += 2
    		elif value == "b":
    			black += 1
    		elif value == "B":
    			black += 2

    if color == 'b':
        return black - white
    else:
        return white - black



class State(object):
	def __init__(self, board, color, depth=-1, value=None):
		self.board = board
		self.color = color
		self.value = value
		self.depth = depth
		self.successors = {}

		# Compute tree of successors with depth 6
		moves = allowed_moves(self.board, self.color)
		self.depth += 1
		for move in moves:
			if self.depth < 6:
				updated_board = update_board(self.board, move, self.color)

				successor = State(updated_board,
								  next_color(self.color),
								  self.depth)
				self.successors[successor] = move


	def __repr__(self):
		return '\n'.join(self.board)

	def set_value(self, value):
		self.value = value


def play(board, color):
	state = State(board, color)
	minimax_score = max_value(state, color)
	for key, move in state.successors.items():
		if key.value == minimax_score:
			return move


def max_value(state, color):
	if len(state.successors) == 0:
		minimax_score = score(state.board, color)
		state.set_value(minimax_score)
		return minimax_score

	else:
		minimax_score = -1e10
		for move in state.successors:
			minimax_score = max(minimax_score, min_value(move, color))
		state.set_value(minimax_score)
		return minimax_score


def min_value(state, color):
	if len(state.successors) == 0:
		minimax_score = score(state.board, color)
		state.set_value(minimax_score)
		return minimax_score

	else:
		minimax_score = 1e10
		for move in state.successors:
			minimax_score = min(minimax_score, max_value(move, color))
		state.set_value(minimax_score)
		return minimax_score


def random_play(board, color):
    """
        An example of play function based on allowed_moves.
    """
    moves = allowed_moves(board, color)
    # There will always be an allowed move
    # because otherwise the game is over and
    # 'play' would not be called by main.py
    return random.choice(moves)
