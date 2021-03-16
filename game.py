import chess
import chess.svg
import utils
from keras.models import load_model
from tkinter import *
from PIL import ImageTk, Image
from chessboard import display
from time import sleep

model = load_model(r'C:\Users\mindf\Documents\WorkandSchool\TKS\Focus\Replicate2\Code\chessai.h5')

board = chess.Board()

def get_move():
    print('================================')
    print('Your Turn! Enter the move here:')
    move = str(input())
    return move

display.start(board.fen())

while True:

    player_move = get_move()
    board.push_san(player_move)
    display.update(board.fen())
    sleep(1)
    if board.is_game_over():
        display.terminate()
        print("\nCONGRATULATIONS! YOU'VE BEAT THE AI!")
        break
    

    print('================================')
    print("Ai's turn...\n")
    move = utils.move_from_ai(board, 1)
    board.push(move)
    sleep(1)
    display.update(board.fen())
    print('\n')
    if board.is_game_over():
        display.terminate()
        print("\nGood game! Try harder next time ;)")
        break