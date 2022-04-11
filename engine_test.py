import engine_main # UCI engine
import chess # chess 
import chess.engine # chess engine
import time # time module
import engine # engine

def test_move():
        """Testing engine"""
        
        _engine = chess.engine.SimpleEngine.popen_uci("./stockfish")
        board = chess.Board()
        
        command = 'go depth 20' # test command
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
                    score = engine.analyze(_engine, board, sdepth)  # score
                else:  # if black to move
                    score = engine.analyze(_engine, board, sdepth)  # score

                usedtime = int((time.time() - start) * 1000)  # time used
                print(
                    'info depth {} score cp {} time {}'.format(sdepth, score, usedtime))  # about thinking

            for m in range(0, 2):  # generate moves. 2 for ponder
                best_move = engine.best_move(_engine, board, sdepth)  # append moves to moves list
                print("bestmove " + str(best_move))  # send response about best move

            # checks for no-bugs
            if movetime > 0 and (time.time() - start) * 1000 > movetime:
                break

            if sdepth >= depth:
                break

        print("bestmove " + str(best_move))

        del best_move  # delete best move

test_move() # starting!
exit() # exiting
