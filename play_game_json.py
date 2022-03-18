import json
import sys

import chess


def play(filename):
    if filename.endswith('.json'):
        game = json.load(open(filename, 'r'))

    else:
        game = json.load(open('r', filename + '.json'))

    game_keys = game.keys()

    board = chess.Board()

    try:
        for key in game_keys:
            board = chess.Board(str(game[key]))
            print(board.unicode())
            print(key)
            print('\n' * 3)

    finally:
        print()


play(sys.argv[1])
