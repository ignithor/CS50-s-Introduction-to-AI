"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    counter_empty = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                counter_empty += 1
    if counter_empty % 2 == 1:
        return (X)
    else:
        return (O)
                

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    available = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                available.add((i, j))
    return (available)


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    available = actions(board)
    if not (action in available):
        raise ValueError("Action not allowed")
    turn = player(board)
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = turn
    return (new_board)


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return (board[i][0])
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return (board[0][i])
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return (board[0][0])
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return (board[0][2])
    return (None)


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    finish = winner(board)
    if finish != None or len(actions(board)) == 0:
        return (True)
    else:
        return (False)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    end = winner(board)
    if end == None:
        return (0)
    elif end == X:
        return (1)
    else:
        return (-1)


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return (None)
    turn = player(board)
    if turn == X:
        # Maximise function
        _, action = maxvalue(board)
        return (action)
    else:
        # Minimise function
        _, action = minvalue(board)
        return (action)


def maxvalue(board):
    v = float('-inf')
    best_action = None
    if terminal(board):
        return (utility(board), None)
    for action in actions(board):
        v_min, _ = minvalue(result(board, action))
        if v < v_min:
            v = v_min
            best_action = action
    return (v, best_action)


def minvalue(board):
    v = float('inf')
    best_action = None
    if terminal(board):
        return (utility(board), None)
    for action in actions(board):
        v_max, _ = maxvalue(result(board, action))
        if v > v_max:
            v = v_max
            best_action = action
    return (v, best_action)