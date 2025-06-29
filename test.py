import copy
from game import startPlannedGame

ROWS = 6
COLUMNS = 7
MAX_DEPTH = 4

def get_valid_moves(board):
    return [c for c in range(COLUMNS) if len(board[c]) < ROWS]

def make_move(board, col, player):
    new_board = copy.deepcopy(board)
    new_board[col].append(player)
    return new_board

def flatten_board(board):
    flat = []
    for i in range(max(len(col) for col in board)):
        for col in board:
            if i < len(col):
                flat.append(col[i])
            else:
                flat.append(0)
    return flat

def board_to_move_sequence(board):
    moves = []
    temp_board = [[] for _ in range(COLUMNS)]
    total_moves = sum(len(col) for col in board)
    for i in range(total_moves):
        for c in range(COLUMNS):
            if len(temp_board[c]) < len(board[c]):
                temp_board[c].append(board[c][len(temp_board[c])])
                moves.append(c)
                break
    return moves

def evaluate(board, player):
    # Vereinfachte Bewertungsfunktion
    opponent = 2 if player == 1 else 1
    return score_position(board, player) - score_position(board, opponent)

def score_position(board, player):
    # Zähle Gruppen von 2 oder 3 gleichen in horizontaler Richtung (vereinfachte Heuristik)
    score = 0
    # Horizontal scannen
    for row in range(ROWS):
        row_array = []
        for col in range(COLUMNS):
            if row < len(board[col]):
                row_array.append(board[col][row])
            else:
                row_array.append(0)
        for c in range(COLUMNS - 3):
            window = row_array[c:c+4]
            score += evaluate_window(window, player)
    return score

def evaluate_window(window, player):
    score = 0
    opponent = 2 if player == 1 else 1
    if window.count(player) == 4:
        score += 100
    elif window.count(player) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(player) == 2 and window.count(0) == 2:
        score += 2
    if window.count(opponent) == 3 and window.count(0) == 1:
        score -= 4
    return score

def is_terminal_node(board):
    moves = board_to_move_sequence(board)
    winner = startPlannedGame(moves)
    return winner != 0 or all(len(col) == ROWS for col in board)

def minimax(board, depth, maximizingPlayer, player):
    valid_locations = get_valid_moves(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        moves = board_to_move_sequence(board)
        winner = startPlannedGame(moves)
        if winner == player:
            return (None, float('inf'))
        elif winner == 0:
            return (None, 0)
        elif winner != 0:
            return (None, float('-inf'))
        return (None, evaluate(board, player))

    if maximizingPlayer:
        value = float('-inf')
        best_col = valid_locations[0]
        for col in valid_locations:
            new_board = make_move(board, col, player)
            new_score = minimax(new_board, depth-1, False, player)[1]
            if new_score > value:
                value = new_score
                best_col = col
        return best_col, value
    else:
        opponent = 2 if player == 1 else 1
        value = float('inf')
        best_col = valid_locations[0]
        for col in valid_locations:
            new_board = make_move(board, col, opponent)
            new_score = minimax(new_board, depth-1, True, player)[1]
            if new_score < value:
                value = new_score
                best_col = col
        return best_col, value

def best_move(board, player):
    col, _ = minimax(board, MAX_DEPTH, True, player)
    return col

board = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
for row in board:
    row = [zahl for zahl in row if zahl != 4]

move = best_move(board, 1)