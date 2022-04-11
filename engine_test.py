import engine_main # Training agent
import chess # chess 
import chess.engine # chess engine

def test_move():
    """Testing training"""
    test_board = chess.Board() # tests board
    _engine = chess.engine.SimpleEngine.popen_uci("./stockfish") # openning engine
    engine_main.go(command="go depth 20", engine=_engine, board=test_board,
                   depth=20) # start training

test_move() # starting!
