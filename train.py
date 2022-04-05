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
from python_checking import check # checking Operating System

init(autoreset=True) # initing colorama

coloredlogs.install(level='INFO') # installing colored logs on INFO level

logger = logging.getLogger("MarcoEngineTraining") # logger

uci_conf = json.load(open('./settings/uci_config.json', 'r')) # uci config
train_conf = json.load(open('./settings/train_conf.json', 'r')) # train config
conf = json.load(open("./settings/conf.json", "r")) # main config
results_dictionary = json.load(open("./games/results.json", "r")) # results of training games
now_game_playing = json.load(open("./in_play/now_playing.json", "r")) # now game in platying
games_count = train_conf['Games count'] # Games count(played)
games_count_for_train = conf["Games Train Count"] # Games count(for train)

def show_intro():
    """Showing intro"""
    intro = Fore.RED + """                                                                      
_|_|_|_|_|                      _|            _|                      
    _|      _|  _|_|    _|_|_|      _|_|_|        _|_|_|      _|_|_|  
    _|      _|_|      _|    _|  _|  _|    _|  _|  _|    _|  _|    _|  
    _|      _|        _|    _|  _|  _|    _|  _|  _|    _|  _|    _|  
    _|      _|          _|_|_|  _|  _|    _|  _|  _|    _|    _|_|_|  
                                                                  _|  
                                                              _|_|
    ----------------------------------------------------------------
                                                            """ # intro

    print(intro) # printing entro


# anti-jit-errors
def analyze_antijit(info, uci_conf):
    """Thats be for non bugs with numba, but now, we not using numba"""
    info['Hash'] = uci_conf['Hash']  # hash
    info['MultiPV'] = uci_conf['MultiPV']  # multipv
    info['nodes'] = uci_conf['nodes']  # nodes of game


def analyze(engine, board, depth: int = None, limit: int = None):
    """Analyzing(score)"""
    if depth is None and limit is None: # if depth and limit is none(empty)
        raise 'You want input depth or limit!' # raised error

    elif depth is not None and limit is None: # if depth is not none, but limit is none
        info = engine.analyse(board, chess.engine.Limit(depth=depth)) # analyzing on depth

        analyze_antijit(info, uci_conf) # anti-jit sets

        return info['score'] # returns score

    elif depth is None and limit is not None: # if depth is none, but limit is not none
        info = engine.analyse(board, chess.engine.Limit(time=limit)) # analyzing on limit

        analyze_antijit(info, uci_conf) # anti-jit sets

        return info['score'] # returns score


def analyze_without_score(engine, board, depth: int = None, limit: int = None):
    """Analyzing(without score)"""
    if depth is None and limit is None: # if depth and limit is none(empty)
        raise 'You want input depth or limit!' # raised error

    elif depth is not None and limit is None: # if depth is not none, but limit is none
        info = engine.analyse(board, chess.engine.Limit(depth=depth)) # analyzing on depth

        analyze_antijit(info, uci_conf) # anti-jit sets

        return info['score'] # returns score

    elif depth is None and limit is not None: # if depth is none, but limit is not none
        info = engine.analyse(board, chess.engine.Limit(time=limit)) # analyzing on limit

        analyze_antijit(info, uci_conf) # anti-jit sets

        return info['score'] # returns score
        
def best_move(engine, board: chess.Board, depth: int = None, limit: int = None, use_weights = True):
    """Returns best move"""

    if use_weights: # if we using weights
        scores_dict = {} # scores dictionary

        for w in os.listdir(str('./weights')): # cycle of weights 
            weights_json = json.load(open(f"weights/{w}", 'r')) # weights openning

            result = engine.play(board, chess.engine.Limit(depth=depth)) # default move 

            if str(board.shredder_fen()) not in weights_json.values():  # if board in weights
                now_game_playing[str(result.move)] = str(board.shredder_fen()) # added move to now playing game

                with open('./in_play/now_playing.json', 'w') as playing_game:  # openning weights file
                    json.dump(now_game_playing, playing_game, indent=4)  # dump dictionary to weights file

                return result.move # returns move

            else:
                result = get_key(weights_json, str(board.shredder_fen())) # be 

                board.push(chess.Move.from_uci(str(result))) # making move
                score = analyze(engine=engine, board=board, depth=DEFAULT_DEPTH - 5) # analyzing
                scores_dict[str(result.move)] = str(score) # append score and move to dictionary

                board.pop() # undo move
                
        if board.turn: # if white to move
            now_game_playing[str(result.move)] = str(board.shredder_fen()) # added move to now playing game
            with open('./in_play/now_playing.json', 'w') as playing_game:  # openning weights file
                json.dump(now_game_playing, playing_game, indent=4)  # dump dictionary to weights file

            return str(get_key(scores_dict, max(scores_dict.values()))) # returns move with maximal score 

        else: # if black to move
            now_game_playing[str(result.move)] = str(board.shredder_fen()) # added move to now playing game
            with open('./in_play/now_playing.json', 'w') as playing_game:  # openning weights file
                json.dump(now_game_playing, playing_game, indent=4)  # dump dictionary to weights file

            return str(get_key(scores_dict, min(scores_dict.values()))) # returns move with minimal score 
        
    else: # if we not using
        if depth is None and limit is None: # if depth and limit is none(empty)
            raise 'You want input depth or limit!' # raised error

        elif depth is not None and limit is None: # if depth is not none, but limit is none 
            result = engine.play(board, chess.engine.Limit(depth=depth)) # move

            return result.move # return move

        elif depth is None and limit is not None:
            result = engine.play(board, chess.engine.Limit(time=limit)) # move

            return result.move # return move

def get_move(board, depth, use_weights):
    """Getting best move. Help if you using Lichess bot."""
    engine = chess.engine.SimpleEngine.popen_uci(ENGINE_DIR)  # engine

    if use_weights:
        try: # trying
            move = best_move(engine=engine, board=board, depth=depth, use_weights=True) # getting best move

        except: # if error
            move = best_move(engine=engine, board=board, depth=depth, use_weights=False) # getting move

    else:
        move = best_move(engine=engine, board=board, depth=depth, use_weights=False) # getting move
        
    board.push(move) # making move

    print_o(move)  # prints move
    if board.is_game_over(): # if game over

        create_new_move(filename='./in_play/now_playing.json') # genering weights on played game

    engine.close()

def create_new_move(filename):
    """Generate weights"""
    if filename.endswith('.json'): # if file is ends with .json
        dict_errors = json.load(open(filename, 'r')) # openning game
        
    else: # if file not ends with .json
        dict_errors = json.load(open(filename + '.json', 'r')) # openning game

    engine = chess.engine.SimpleEngine.popen_uci(ENGINE_DIR) # openning engine

    start_time = time.perf_counter() # start time

    w_ = 0 # weights iteration

    for w in os.listdir(str('./weights')): # cycle of weights
        dict_norm = json.load(open(f"weights/{w}", 'r')) # openning weights

        w_ += 1 # +1 to weights iteration

        error_keys = dict_errors.keys() # error moves

        fens = [] # fens list
        dict_moves = [] # moves list
        dict_keys = [] # keys list

        for key in tqdm(error_keys, desc=f"Generating weights {w_}"): # custom cycle of iteation weights
            board = chess.Board(dict_errors[key]) # board on fen
            score = analyze(engine=engine, board=board, depth=DEFAULT_DEPTH) # score
            real_score = re.sub('\D', '', str(score)) # real score(replacing)

            if '-' in str(score) and int(str('-') + str(real_score)) <= -40: # if score is very negative
                move = best_move(engine=engine, board=board, depth=DEFAULT_DEPTH) # move 

                if not move is None: # if move is not none
                    try: # trying
                        try: # trying
                            board.push(move) # pushing move

                        except: # if error
                            move = best_move(engine=engine, board=board, depth=DEFAULT_DEPTH, use_weights=False) # analyzing move without weights
                            board.push(move) # pushing move
                    
                    except: # if error
                        try: # trying
                            board.push(chess.Move.from_uci(str(move))) # pushing move

                        except: # if error
                            move = best_move(engine=engine, board=board, depth=DEFAULT_DEPTH, use_weights=False) # analyzing move without weights
                            board.push(move) # pushing move

                    fens.append(str(board.shredder_fen())) # append shredder fen to fens list
                    dict_moves.append(str(move)) # append move to moves
                    dict_keys.append(str(key)) # append key to keys

                else: # if move is none
                    move = best_move(engine, board, depth=DEFAULT_DEPTH, use_weights=False) # analyzing move without move
                    board.push(move) # pushing move

                    fens.append(str(board.shredder_fen())) # append shredder fen to fens list
                    dict_moves.append(str(move)) # append move to moves
                    dict_keys.append(str(key)) # append key to keys

            if '+' in str(score) and int(real_score) >= 40:
                move = best_move(engine=engine, board=board, depth=DEFAULT_DEPTH) # move 

                if not move is None: # if move is not none
                    try: # trying
                        try: # trying
                            board.push(move) # pushing move

                        except: # if error
                            move = best_move(engine=engine, board=board, depth=DEFAULT_DEPTH, use_weights=False) # analyzing move without weights
                            board.push(move) # pushing move
                    
                    except: # if error
                        try: # trying
                            board.push(chess.Move.from_uci(str(move))) # pushing move

                        except: # if error
                            move = best_move(engine=engine, board=board, depth=DEFAULT_DEPTH, use_weights=False) # analyzing move without weights
                            board.push(move) # pushing move

                    fens.append(str(board.shredder_fen())) # append shredder fen to fens list
                    dict_moves.append(str(move)) # append move to moves
                    dict_keys.append(str(key)) # append key to keys

                else: # if move is none
                    move = best_move(engine, board, depth=DEFAULT_DEPTH, use_weights=False) # analyzing move without move
                    board.push(move) # pushing move

                    fens.append(str(board.shredder_fen())) # append shredder fen to fens list
                    dict_moves.append(str(move)) # append move to moves
                    dict_keys.append(str(key)) # append key to keys

            for _move in dict_moves:
                dict_norm[str(move)] = fens[dict_moves.index(_move)]
        
        model_number = random.randrange(0, 1000000) # weights model number

        with open(f'weights/weights_norm_{model_number}.json', 'w') as weights_file: # openning weights file
            json.dump(dict_norm, weights_file, indent=4) # dump dictionary to weights file

    end_time = time.perf_counter() # end time

    engine.quit()

    return end_time - start_time # returns elapsed time


def train(engine, board):
    """Trains MarcoEngine"""
    dictionary = {} # game dictionary
    board_ = new_board(old_board=board) # creating new board

    start_time = time.perf_counter() # start time

    while not board_.is_game_over(): # cycle. ends if game is over
   
        try: # trying
            move = best_move(engine=engine, board=board_, depth=DEFAULT_DEPTH) # best move

            dictionary[str(move)] = str(board_.shredder_fen()) # append move and shredder fen to game dictionary
            
            board_.push(chess.Move.from_uci(str(move))) # pushing move

        except: # if error
            move = best_move(engine=engine, board=board_, limit=DEFAULT_DEPTH, use_weights=False) # analyzing move without weights

            dictionary[str(move)] = str(board_.shredder_fen()) # append move and shredder fen to game dictionary
            
            board_.push(move) # pushing move


        #board_ = new_board(old_board=board_, fen=board_.fen()) # update board

    end_time = time.perf_counter() # end time

    train_conf['Games count'] = train_conf['Games count'] + 1 # +1 to games trained
    json.dump(train_conf, open('./settings/train_conf.json', 'w')) # dumps it


    return board_, dictionary, end_time - start_time # returns board, game and elapsed time


def results_print(i, results_dict):
    """Printing iteration self-playing results"""
    draws = 0 # draws
    wins_w = 0 # white wins
    wins_b = 0 # black wins

    for result in list(results_dict.keys()): # cycle of result in  results
        if "1/2-1/2" in result: # if draw in result
            draws += 1 # +1 to draws

        elif "1-0" in result: # if white win in results
            wins_w += 1 # +1 to white wins

        elif "0-1" in result: # if black win in resuls
            wins_b += 1 # +1 to black wins

    print('\n' * 2) # two enters

    table = Table(title="Train results") # creating table

    table.add_column("Iteration", justify="right", style="cyan", no_wrap=True) # iteration
    table.add_column("Played games", justify="right", style="cyan", no_wrap=True) # played games
    table.add_column("Wins white", style="magenta") # white wins
    table.add_column("Wins black", style="magenta") # black wins
    table.add_column("Draws", style="magenta") # draws

    table.add_row(str(i), str(len(results_dict.keys())), str(wins_w), str(wins_b), str(draws)) # adding rows to table

    console = Console() # openning rich's console
    console.print(table) # printing table


def start(engine, g):
    """Starts train"""
    global path # be path of game global

    path = "./games/game" + str(random.randint(0, 1000000)) + '.json' # path of games
    b, _dictionary, elapsed = train(engine=engine, board=_board) # board, game dictionary and elapsed time

    with open(path, "w") as write_file: # openning game path
        json.dump(_dictionary, write_file, indent=4) # dump games dictionary to path

    return b.result() # returns board result


if __name__ == '__main__': # if we start THIS file
    show_intro()  # showing intro
    check() # checking Operating system

    count_g = 0 # games count
    iteration = 0 # number of iteration

    while True: # endless cycle
        iteration += 1 # +1 to iteration

        _board = chess.Board() # board

        for _ in tqdm(range(0, games_count_for_train), desc="Self Play"): # self playing
            count_g += 1 # +1 to games count

            engine = chess.engine.SimpleEngine.popen_uci(ENGINE_DIR) # engine
            
            resul = start(engine=engine, g=count_g) # starting game
            engine.quit() # engine exit

            results_dictionary[str(count_g) + " " + str(resul)] = " " # apenning game result to result's dictionary

            with open('./games/results.json', "w") as results_diictionary: # openning results dictionary
                json.dump(results_dictionary, results_diictionary) # dump dictionary to results

        engine = chess.engine.SimpleEngine.popen_uci(ENGINE_DIR) # openning engine
        create_new_move(filename=path) # creating new move

        results_print(i=iteration, results_dict=results_dictionary) # printing train results
        print() # enter

        os.system("rm games/*") # deleting from games all files
        print_l("Games cleared!") # printing about that
        
        del results_dictionary # deleting results
        
        results_dictionary = json.load(create_file("games/results.json")) # creating new file of results
        print_l("New results created!") # printing about that
        print() # enter
