"""
Tic Tac Toe Player
"""
import copy
import math
import sys

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
    xCount = 0
    oCount = 0
    for row in board:
        for cell in row:
            xCount = xCount + (1 if cell == X else 0)
            oCount = oCount + (1 if cell == O else 0)
    return X if xCount == oCount else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    availableActions = set()    
    for rowIndex in range(3):
        for columnIndex in range(3):
            if board[rowIndex][columnIndex] == EMPTY:
                availableActions.add((rowIndex, columnIndex))
    return availableActions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] != EMPTY or action[0] > 2 or action[1] > 2 or action[0] < 0 or action[1] < 0:
        raise
    currentPlayer = player(board)
    newBoard = copy.deepcopy(board)
    newBoard[action[0]][action[1]] = currentPlayer
    return newBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if board[i][0] != EMPTY and board[i][0] == board[i][1] and board[i][0] == board[i][2]:
            return board[i][0]
    for j in range(3):
        if board[0][j] != EMPTY and board[0][j] == board[1][j] and board[0][j] == board[2][j]:
            return board[0][j]
    if board[0][0] != EMPTY and board[0][0] == board[1][1] and board[0][0] == board[2][2]:
        return board[0][0]
    if board[0][2] != EMPTY and board[0][2] == board[1][1] and board[0][2] == board[2][0]:
        return board[0][2]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    isFull = True
    for row in board:
        if EMPTY in row:
            isFull = False
            break
    return isFull or (winner(board) != None)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    currentWinner = winner(board)
    return 1 if currentWinner == X else -1 if currentWinner == O else 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    currentPlayer = player(board)
    _, minimaxReturn = maxValue(board) if currentPlayer == X else minValue(board)
    return minimaxReturn

def maxValue(board, boundary=sys.maxsize):
    if terminal(board):
        return utility(board), None
    resultValue = -sys.maxsize - 1
    resultAction = None
    for action in actions(board):
        actionValue, _ = minValue(result(board, action), boundary)
        if actionValue > resultValue:
            resultValue = actionValue
            boundary = resultValue
            resultAction = action
        if actionValue > boundary:
            break
    return resultValue, resultAction

def minValue(board, boundary=-sys.maxsize - 1):
    if terminal(board):
        return utility(board), None
    resultValue = sys.maxsize
    resultAction = None
    for action in actions(board):
        actionValue, _ = maxValue(result(board, action), boundary)
        if actionValue < resultValue:
            resultValue = actionValue
            boundary = resultValue
            resultAction = action
        if actionValue < boundary:
            break
    return resultValue, resultAction