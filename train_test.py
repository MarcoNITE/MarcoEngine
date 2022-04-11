import chess # chess
import chess.engine # chess engine
import train # Training agent

test_board = chess.Board() # our testing board
_engine = chess.engine.SimpleEngine.popen_uci("./stockfish") # engine

train.train(engine=_engine, board=test_board) # starting train
_engine.quit() # quiting from engine
