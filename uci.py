import json # json dictionaries
import os # Operating System
import time # time module

import chess.engine # chess engine
from colorama import init, Fore # color text

import train # train module
from utils import * # utils

init(autoreset=True) # initing colorama

weights = [] # weights list

SHOW_THINKING = True # showing thinking?

board = chess.Board() # board
engine = chess.engine.SimpleEngine.popen_uci("stockfish") # chess engine
uci_conf = json.load(open('./settings/uci_config.json', 'r')) # uci config
uci_conf2 = json.load(open('./settings/conf.json', 'r')) # id's uci config
uci_default_conf = json.load(open('./settings/uci_default_config.json', 'r')) # default uci config
uci_min_conf = json.load(open('./settings/uci_min_config.json', 'r')) # minimal uci config
uci_max_conf = json.load(open('./settings/uci_max_config.json', 'r')) # maximal uci config


def show_intro():
    """Showing intro"""
    intro = Fore.GREEN + f""" _______ _______               __              
|   |   |    ___|.-----.-----.|__|.-----.-----.
|       |    ___||     |  _  ||  ||     |  -__|
|__|_|__|_______||__|__|___  ||__||__|__|_____|
                       |_____|      
-----------------------------------------------
{Fore.MAGENTA} MarcoEngine by Mark Kim. {Fore.LIGHTRED_EX} Neural chess network.  
                       """ # intro

    print(intro) # printing intro


def if_havent_weights(dir):
    """Check for user have weights"""
    dir_list = os.listdir(str(dir)) # dir of list weights
    if dir_list == ["weights_norm.default.json"]: # if dir list is default weights
        print_l("""
                    You want to rename "weights_norm.json"(in directory
                    "weights") to "weights_norm.json".
        
        """, type="CRITICAL") # printing error about


def finding_weights():
    # finding weights file
    for f in os.listdir("./weights"):  # cycle of files in "weights" directory
        if f.endswith(".json"):  # if file ends with ".json"..
            weights.append(json.load(open(f'./weights/{f}', 'r')))  # append to weights that file


def uci_commander(command):
    # UCI-protocol

    if command.startswith('go'):
        # default options
        depth = 1000  # depth
        movetime = -1  # movetime

        # parse values
        _, *params = command.split(' ')  # parameters
        for param, val in zip(*2 * (iter(params),)):  # cycle of params and values
            if param == 'depth':  # depth param
                depth = int(val)  # depth value
            if param == 'movetime':  # movetime param
                movetime = int(val)  # movetime value
            if param == 'wtime':  # wtime param
                our_time = int(val)  # wtime value
            if param == 'btime':  # btime param
                opp_time = int(val)  # btime value

        moves_remain = 40  # remaining moves

        start = time.time()  # start time
        ponder = None  # ponder move
        for sdepth in range(0, depth + 1):  # cycle of self-depth and depth

            if True:  # if showing thinking
                if board.turn:  # if white to move
                    score = train.analyze(engine, board, sdepth)  # score
                else:  # if black to move
                    score = train.analyze(engine, board, sdepth)  # score

                usedtime = int((time.time() - start) * 1000)  # time used
                print(
                    'info depth {} score cp {} time {}'.format(sdepth, score, usedtime))  # about thinking

            for m in range(0, 2):  # generate moves. 2 for ponder
                best_move = train.best_move(engine, board, sdepth)  # append moves to moves list
                print("bestmove " + str(best_move))  # send response about best move

            # checks for no-bugs
            if movetime > 0 and (time.time() - start) * 1000 > movetime:
                break

            if sdepth >= depth:
                break

        print("bestmove " + str(best_move))

        del best_move  # delete best move

    elif command.startswith('uciok') or command == 'uci':  # if command starts with "uciok", or command is "uci"..
        for key in list(uci_conf2.keys()):  # easy config(name, author)
            print(f"id {str(key)}  {uci_conf2[key]}")  # printing

        for key in list(uci_conf.keys()):  # uci config
            type_option = str(type(uci_default_conf[str(key)]))  # type of option
            type_option = type_option.replace("<class '", "")  # deleting <class ' from string
            type_option = type_option.replace("'>", "")  # deleting '> from string
            print(
                f"option name {str(key)} type {type_option} default {uci_default_conf[key]} min {uci_min_conf[key]} max {uci_max_conf[key]}")  # printing

            del type_option  # and deleting

        print('uciok', flush=True)  # uci is ok :)

    elif command.startswith('ucinewgame'):  # if command starts with "ucinewgame"..
        new_board(old_board=board)  # deleting board, create new

    elif command.startswith('position fen'):  # if command starts with "position fen"
        new_board(command.split()[2])  # new board with new fen

    elif command.startswith('position startpos moves'):
        moves = command.split(" ")[3:]  # parse moves
        board.clear()  # clear board
        board.set_fen(chess.STARTING_FEN)  # set starting fen
        for move in moves:  # cycle of moves
            board.push(chess.Move.from_uci(move))  # and make this moves

    elif command.startswith('isready'):  # hey, you ready?
        print('readyok')  # yes, ready

    elif command.startswith('quit'):  # exit
        sys.exit(1)  # exit

    elif command == "":  # random enter
        pass  # passing, new iteration

    else:  # if command unkown...
        print(f'[?] Unknow command: {command}')  # printing


show_intro()  # showing intro
if_havent_weights('./weights')  # check for weights

while True:  # endless cycle
    cmd = input()  # command
    uci_commander(cmd)  # send command
