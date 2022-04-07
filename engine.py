import json # json dictionaries
import os # Operating System
import re # replace string
import time # time module

import chess.engine # chess engine
import coloredlogs # colored logs
from colorama import init, Fore # colored text
from rich.console import Console # Console of rich
from rich.table import Table # rich's colored tables
from tqdm import tqdm # custom cycles

from utils import * # utils
from config import * # config
import train # training agent
from python_checking import check # checking Operating System

coloredlogs.install(level='INFO') # installing colored logs on INFO level

logger = logging.getLogger("Engine") # logger

uci_conf = json.load(open('./settings/uci_config.json', 'r')) # uci config
train_conf = json.load(open('./settings/train_conf.json', 'r')) # train config
conf = json.load(open("./settings/conf.json", "r")) # main config
results_dictionary = json.load(open("./games/results.json", "r")) # results of training games
now_game_playing = json.load(open("./in_play/now_playing.json", "r")) # now game in platying
games_count = train_conf['Games count'] # Games count(played)
games_count_for_train = conf["Games Train Count"] # Games count(for train)

# anti-jit-errors
def analyze_antijit(info, uci_conf):
    """Thats be for non bugs with numba, but now, we not using numba"""
    info['Hash'] = uci_conf['Hash']  # hash
    info['MultiPV'] = uci_conf['MultiPV']  # multipv
    info['nodes'] = uci_conf['nodes']  # nodes of game


def analyze(engine, board, depth: int = None, limit: int = None):
    """Analyzing(score)"""
    if depth is None and limit is None:  # if depth and limit is none(empty)
        raise 'You want input depth or limit!'  # raised error

    elif depth is not None and limit is None:  # if depth is not none, but limit is none
        info = engine.analyse(board, chess.engine.Limit(depth=depth))  # analyzing on depth

        analyze_antijit(info, uci_conf)  # anti-jit sets

        return info['score']  # returns score

    elif depth is None and limit is not None:  # if depth is none, but limit is not none
        info = engine.analyse(board, chess.engine.Limit(time=limit))  # analyzing on limit

        analyze_antijit(info, uci_conf)  # anti-jit sets

        return info['score']  # returns score


def analyze_without_score(engine, board, depth: int = None, limit: int = None):
    """Analyzing(without score)"""
    if depth is None and limit is None:  # if depth and limit is none(empty)
        raise 'You want input depth or limit!'  # raised error

    elif depth is not None and limit is None:  # if depth is not none, but limit is none
        info = engine.analyse(board, chess.engine.Limit(depth=depth))  # analyzing on depth

        analyze_antijit(info, uci_conf)  # anti-jit sets

        return info['score']  # returns score

    elif depth is None and limit is not None:  # if depth is none, but limit is not none
        info = engine.analyse(board, chess.engine.Limit(time=limit))  # analyzing on limit

        analyze_antijit(info, uci_conf)  # anti-jit sets

        return info['score']  # returns score


def best_move(engine, board: chess.Board, depth: int = None, limit: int = None, use_weights=True):
    """Returns best move"""

    if use_weights:  # if we using weights
        scores_dict = {}  # scores dictionary

        for w in os.listdir(str('./weights')):  # cycle of weights
            weights_json = json.load(open(f"weights/{w}", 'r'))  # weights openning

            result = engine.play(board, chess.engine.Limit(depth=depth))  # default move

            if str(board.shredder_fen()) not in weights_json.values():  # if board in weights
                now_game_playing[str(result.move)] = str(board.shredder_fen())  # added move to now playing game

                with open('./in_play/now_playing.json', 'w') as playing_game:  # openning weights file
                    json.dump(now_game_playing, playing_game, indent=4)  # dump dictionary to weights file

                return result.move  # returns move

            else:
                result = get_key(weights_json, str(board.shredder_fen()))  # be

                board.push(chess.Move.from_uci(str(result)))  # making move
                score = analyze(engine=engine, board=board, depth=DEFAULT_DEPTH - 5)  # analyzing
                scores_dict[str(result.move)] = str(score)  # append score and move to dictionary

                board.pop()  # undo move

        if board.turn:  # if white to move
            now_game_playing[str(result.move)] = str(board.shredder_fen())  # added move to now playing game
            with open('./in_play/now_playing.json', 'w') as playing_game:  # openning weights file
                json.dump(now_game_playing, playing_game, indent=4)  # dump dictionary to weights file

            return str(get_key(scores_dict, max(scores_dict.values())))  # returns move with maximal score

        else:  # if black to move
            now_game_playing[str(result.move)] = str(board.shredder_fen())  # added move to now playing game
            with open('./in_play/now_playing.json', 'w') as playing_game:  # openning weights file
                json.dump(now_game_playing, playing_game, indent=4)  # dump dictionary to weights file

            return str(get_key(scores_dict, min(scores_dict.values())))  # returns move with minimal score

    else:  # if we not using
        if depth is None and limit is None:  # if depth and limit is none(empty)
            raise 'You want input depth or limit!'  # raised error

        elif depth is not None and limit is None:  # if depth is not none, but limit is none
            result = engine.play(board, chess.engine.Limit(depth=depth))  # move

            return result.move  # return move

        elif depth is None and limit is not None:
            result = engine.play(board, chess.engine.Limit(time=limit))  # move

            return result.move  # return move


def get_move(board, depth, use_weights):
    """Getting best move. Help if you using Lichess bot."""
    engine = chess.engine.SimpleEngine.popen_uci(ENGINE_DIR)  # engine

    if use_weights:
        try:  # trying
            move = best_move(engine=engine, board=board, depth=depth, use_weights=True)  # getting best move

        except:  # if error
            move = best_move(engine=engine, board=board, depth=depth, use_weights=False)  # getting move

    else:
        move = best_move(engine=engine, board=board, depth=depth, use_weights=False)  # getting move

    board.push(move)  # making move

    print_o(move)  # prints move
    if board.is_game_over():  # if game over

        train.create_new_move(filename='./in_play/now_playing.json')  # genering weights on played game

    engine.close()

if __name__ == '__main__': # if we start THIS file
    check() # checking Operating system