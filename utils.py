import chess
from tensorflow import keras
from keras.models import Model
import numpy as np
from keras.models import load_model

model = load_model(r'C:\Users\mindf\Documents\WorkandSchool\TKS\Focus\Replicate2\Code\chessai.h5')


def predictions_for_minimax(board):

    board_3d = dimension_split(board)
    board_3d = np.expand_dims(board_3d, 0)
    return model.predict(board_3d)[0][0]

def minimax(board, depth, a, b, max_player):

    if depth == 0 or board.is_game_over():
        return predictions_for_minimax(board)

    if max_player:
        max_eval = -np.inf
        for move in board.legal_moves:
            board.push(move)
            score_eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, score_eval)
            alpha = max(alpha, max_eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = np.inf
        for move in board.legal_moves:
            board.push(move)
            score_eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, score_eval)
            beta = min(beta, score_eval)
            if beta <= alpha:
                break
        return min_eval

def move_from_ai(board, depth):
    max_move = None
    max_eval = -np.inf

    for move in board.legal_moves:
        board.push(move)
        eval = minimax(board, depth - 1, -np.inf, np.inf, False)
        board.pop()
        if eval > max_eval:
            max_eval = eval
            max_move = move
    return max_move

#Encoding each piece to a number (dictionary)

index_of_pieces = {'a':0, 'b':1, 'c':2, 'd':3, 'e':4, 'f':5, 'g':6, 'h':7}

def score_from_stockfish(board, depth):
    with chess.engine.SimpleEngine.popen_uci(r'C:\Users\mindf\Documents\WorkandSchool\TKS\Focus\Replicate2\Code\stockfish_13_win_x64_bmi2\stockfish_13_win_x64_bmi2.exe') as stockfish:

        output = stockfish.analyse(board, chess.engine.Limit(depth = depth))
        score = output['score'].white().score()
        return score

#Turning a chess coordinate to a number
def sq_2_index(square):
    letter = chess.square_name(square)
    return 8 - int(letter[1]), index_of_pieces[letter[0]]

def dimension_split(board):

    board_3d = np.zeros((14,8,8), dtype = np.int8)

    for piece in chess.PIECE_TYPES:
        for square in board.pieces(piece, chess.WHITE):
            index = np.unravel_index(square,(8,8))
            board_3d[piece - 1][7 - index[0]][index[1]] = 1
        for square in board.pieces(piece, chess.BLACK):
            index = np.unravel_index(square,(8,8))
            board_3d[piece - 1][7 - index[0]][index[1]] = 1
    
    #attacks, legal moves
    aux = board.turn
    board.turn = chess.WHITE
    for move in board.legal_moves:
        i, j = sq_2_index(move.to_square)
        board_3d[12][i][j] = 1
    board.turn = chess.BLACK
    for move in board.legal_moves:
        i, j = sq_2_index(move.to_square)
        board_3d[13][i][j] = 1
    board.turn = aux

    return board_3d