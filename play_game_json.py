import json # json dictionaries
import sys # system

import chess # chess


def play(filename):
    """Playing a game"""
    if filename.endswith('.json'): # if file is ended with .json...
        game = json.load(open(filename, 'r')) # loading game

    else: # else
        game = json.load(open('r', filename + '.json')) # loading game

    game_keys = game.keys() # game moves

    board = chess.Board() # chess board

    try: # trying
        for key in game_keys: # cycle of moves
            board = chess.Board(str(game[key])) # sets board with keys
            print(board.unicode()) # printing board with unicode
            print(key) # printing move 
            print('\n' * 3) # enters

    finally: # and finally...
        print() # enter


play(sys.argv[1]) # plays a game on args of game
