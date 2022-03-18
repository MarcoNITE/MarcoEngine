import json
import os
import re
import time

import chess.engine
import coloredlogs
from colorama import init, Fore
from rich.console import Console
from rich.table import Table
from tqdm import tqdm

from utils import *

init(autoreset=True)

coloredlogs.install(level='INFO')

logger = logging.getLogger("MarcoEngineTraining")

logger_ = logging.getLogger("numba")
logger_.setLevel(logging.INFO)



uci_conf = json.load(open('./settings/uci_config.json', 'r'))
train_conf = json.load(open('./settings/train_conf.json', 'r'))
conf = json.load(open("./settings/conf.json", "r"))
results_dictionary = json.load(open("./games/results.json", "r"))
games_count = train_conf['Games count']
games_count_for_train = conf["Games Train Count"]


# graphic
def show_intro():
    intro = Fore.RED + """                                                                      
_|_|_|_|_|                      _|            _|                      
    _|      _|  _|_|    _|_|_|      _|_|_|        _|_|_|      _|_|_|  
    _|      _|_|      _|    _|  _|  _|    _|  _|  _|    _|  _|    _|  
    _|      _|        _|    _|  _|  _|    _|  _|  _|    _|  _|    _|  
    _|      _|          _|_|_|  _|  _|    _|  _|  _|    _|    _|_|_|  
                                                                  _|  
                                                              _|_|
    ----------------------------------------------------------------
                                                            """

    print(intro)


# anti-jit-errors
def analyze_antijit(info, uci_conf):
    """Thats be for non bugs with numba, but now, we no using numba"""
    info['Hash'] = uci_conf['Hash']  # hash
    info['MultiPV'] = uci_conf['MultiPV']  # multipv
    info['nodes'] = uci_conf['nodes']  # nodes of game


# engine utils
def analyze(engine, board, depth: int = None, limit: int = None):
    if depth is None and limit is None:
        return

    elif depth is not None and limit is None:
        info = engine.analyse(board, chess.engine.Limit(depth=depth))

        analyze_antijit(info, uci_conf)

        return info['score']

    elif depth is None and limit is not None:
        info = engine.analyse(board, chess.engine.Limit(time=limit))

        analyze_antijit(info, uci_conf)

        return info['score']


def analyze_without_score(engine, board, depth: int = None, limit: int = None):
    if depth is None and limit is None:
        print_l('You want input depth or limit!')

        return

    elif depth is not None and limit is None:
        info = engine.analyse(board, chess.engine.Limit(depth=depth))

        analyze_antijit(info, uci_conf)

        return info['score']

    elif depth is None and limit is not None:
        info = engine.analyse(board, chess.engine.Limit(time=limit))

        analyze_antijit(info, uci_conf)

        return info


def best_move(engine, board: chess.Board, depth: int = None, limit: int = None, use_weights = True):
    for w in os.listdir(str('./weights')):
        weights_json = json.load(open(f"weights/{w}", 'r'))

        if depth is None and limit is None:
            print_l('You want input depth or limit!')

            return

        elif depth is not None and limit is None:
            result = engine.play(board, chess.engine.Limit(depth=depth))

            if use_weights:
                if  str(board.shredder_fen()) not in weights_json.values():

                    return result.move

                else:

                    result = get_key(weights_json, str(board.shredder_fen()))

                    return result

            return result.move

        elif depth is None and limit is not None:
            result = engine.play(board, chess.engine.Limit(time=limit))

            if use_weights:
                if  str(board.shredder_fen()) not in weights_json.values():

                    return result.move

                else:

                    result = get_key(weights_json, str(board.shredder_fen()))

                    return result

            return result.move




# engine
def create_new_move(filename):
    if filename.endswith('.json'):
        dict_errors = json.load(open(filename, 'r'))


    else:

        dict_errors = json.load(open(filename + '.json', 'r'))

    start_time = time.perf_counter()

    w_ = 0

    for w in os.listdir(str('./weights')):
        dict_norm = json.load(open(f"weights/{w}", 'r'))

        w_ += 1


        error_keys = dict_errors.keys()

        fens = []
        dict_moves = []
        dict_keys = []

        for key in tqdm(error_keys, desc=f"Generating weights {w_}"):
            board = chess.Board(dict_errors[key])
            score = analyze(engine=engine, board=board, depth=20)
            real_score = re.sub('\D', '', str(score))

            if '-' in str(score) and int(str('-') + str(real_score)) <= -40:
                # generating new move
                move = best_move(engine=engine, board=board, depth=20)

                if not move is None:
                    try:
                        try:
                            board.push(move)

                        except:
                            move = best_move(engine=engine, board=board, depth=20, use_weights=False)
                            board.push(move)
                    
                    except:
                        try:
                            board.push(chess.Move.from_uci(str(move)))

                        except:
                            move = best_move(engine=engine, board=board, depth=20, use_weights=False)
                            board.push(move)

                    fens.append(str(board.shredder_fen()))
                    dict_moves.append(str(move))
                    dict_keys.append(str(key))

                else:
                    move = best_move(engine, board, depth=20, use_weights=False)
                    board.push(move)

                    fens.append(str(board.shredder_fen()))
                    dict_moves.append(str(move))
                    dict_keys.append(str(key))

            if '+' in str(score) and int(real_score) >= 40:
                # generating new move
                move = best_move(engine=engine, board=board, depth=20)

                if not move is None:
                    try:
                        try:
                            board.push(move)

                        except:
                            move = best_move(engine=engine, board=board, depth=20, use_weights=False)
                            board.push(move)
                    
                    except:
                        try:
                            board.push(chess.Move.from_uci(str(move)))

                        except:
                            move = best_move(engine=engine, board=board, depth=20, use_weights=False)
                            board.push(move)

                    fens.append(str(board.shredder_fen()))
                    dict_moves.append(str(move))
                    dict_keys.append(str(key))

                else:
                    move = best_move(engine, board, depth=20, use_weights=False)
                    board.push(move)

                    fens.append(str(board.shredder_fen()))
                    dict_moves.append(str(move))
                    dict_keys.append(str(key))

            for _move in dict_moves:
                dict_norm[str(move)] = fens[dict_moves.index(_move)]
        
        model_number = random.randrange(0, 1000000)

        with open(f'weights/weights_norm_{model_number}.json', 'w') as weights_file:
            json.dump(dict_norm, weights_file, indent=4)

    end_time = time.perf_counter()

    return end_time - start_time


def train(engine, board):
    dictionary = {}  # or dict()
    board_ = new_board(old_board=board)

    start_time = time.perf_counter()

    while not board_.is_game_over():
        move = best_move(engine=engine, board=board_, limit=0.001)
        
        dictionary[str(move)] = str(board_.shredder_fen())
        try:
            board_.push(chess.Move.from_uci(str(move)))

        except:
            move = best_move(engine=engine, board=board_, limit=0.001, use_weights=False)
            board_.push(move)

        board_ = new_board(old_board=board_, fen=board_.fen())

    end_time = time.perf_counter()

    train_conf['Games count'] = train_conf['Games count'] + 1
    json.dump(train_conf, open('./settings/train_conf.json', 'w'))


    return board_, dictionary, end_time - start_time


def results_print(i, results_dict):
    draws = 0
    wins_w = 0
    wins_b = 0

    for result in list(results_dict.keys()):
        if "1/2-1/2" in result:
            draws += 1

        elif "1-0" in result:
            wins_w += 1

        elif "0-1" in result:
            wins_b += 1

    print('\n' * 2)

    table = Table(title="Train results")

    table.add_column("Iteration", justify="right", style="cyan", no_wrap=True)
    table.add_column("Played games", justify="right", style="cyan", no_wrap=True)
    table.add_column("Wins white", style="magenta")
    table.add_column("Losses white", style="magenta")
    table.add_column("Draws", style="magenta")

    table.add_row(str(i), str(len(results_dict.keys())), str(wins_w), str(wins_b), str(draws))

    console = Console()
    console.print(table)


def start(engine, g):
    global path

    path = "./games/game" + str(random.randint(0, 1000000)) + '.json'
    b, _dictionary, elapsed = train(engine=engine, board=_board)

    with open(path, "w") as write_file:
        json.dump(_dictionary, write_file, indent=4)

    return b.result()


if __name__ == '__main__':
    show_intro()  # showing intro

    count_g = 0
    iteration = 0

    while True:
        iteration += 1

        _board = chess.Board()

        for _ in tqdm(range(0, games_count_for_train), desc="Self Play"):
            count_g += 1
            engine = chess.engine.SimpleEngine.popen_uci('stockfish')
            resul = start(engine=engine, g=count_g)
            engine.quit()

            results_dictionary[str(count_g) + " " + str(resul)] = " "

            with open('./games/results.json', "w") as results_diictionary:
                json.dump(results_dictionary, results_diictionary)

        engine = chess.engine.SimpleEngine.popen_uci('stockfish')
        create_new_move(filename=path)
        engine.quit()

        results_print(i=iteration, results_dict=results_dictionary)
        print()

        os.system("rm games/*")
        print_l("Games cleared!")
        del results_dictionary
        results_dictionary = json.load(create_file("games/results.json"))
        print_l("New results created!")
        print()
