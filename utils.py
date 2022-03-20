import logging
import random
import sys

import chess

logger = logging.getLogger("MarcoEngine")  # logger


def print_l(msg, type="INFO"):  # print with logger
    if type == "INFO":  # info
        logger.info(msg)  # send

    elif type == "WARN":  # warning
        logger.warning(msg)  # send

    elif type == "ERROR":  # error
        logger.error(msg)  # send

    elif type == "CRITICAL":  # critical error
        logger.critical(msg)  # send
        sys.exit(1)  # exit
        exit(1)  # exit-2


def create_file(name):  # create new file
    a = open(name, "w")  # openning file
    a.write('{}')  # write to file "{}"(for json support)

    return open(name, "r")  # return reading openned file


def new_board(old_board: chess.Board, fen: str = None): 
    """Creating new board"""
    
    if fen is None: # if fen is None(we haven't fen)
        n_board = chess.Board() # new board
        n_board.clear() # clearing board
        n_board.set_fen(chess.STARTING_FEN) # sets startong fen

        return n_board # and returns board

    else: # else
        n_board = chess.Board() # board
        n_board.set_fen(fen) # sets fen

        return n_board # and returns board


def get_key(d, value):
    """Generate key from value"""
    for k, v in d.items(): # cycle of items in dict
        if v == value: # if v is value
            return k # returns key

  
def calculate_time(wtime, btime, depth):
    """Calculate time limit on depth"""
    if wtime <= 1000 and btime >= 1000: # if white is flags
        return "0.{}".format(int(depth // 4)) # returns time

    elif wtime <= 1000 and btime <= 1000: # if white and black is flags
        return "0.".format(int(depth // random.randint(3, 5))) # returns time

    else: # if time is normal
        return "0.".format(int(depth // random.randint(5, 9))) # returns time
