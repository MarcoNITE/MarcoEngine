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


def new_board(old_board: chess.Board, fen: str = None):  # create new board

    if fen is None:
        n_board = chess.Board()
        n_board.clear()
        n_board.set_fen(chess.STARTING_FEN)

        return n_board

    else:
        n_board = chess.Board()
        n_board.set_fen(fen)

        return n_board


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k

  
def calculate_time(wtime, btime, depth):
    if wtime <= 1000 and btime >= 1000:
        return "0.{}".format(int(depth // 4))

    elif wtime <= 1000 and btime <= 1000:
        return "0.".format(int(depth // random.randint(3, 5)))

    else:
        return "0.".format(int(depth // random.randint(5, 9)))
