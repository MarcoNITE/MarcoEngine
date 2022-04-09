import train # Training agent
import chess # chess 
import chess.engine # chess engine

def test_train():
    """Testing training"""
    test_board = chess.Board() # tests board
    _engine = chess.engine.SimpleEngine.popen_uci("./TEMP/sf") # openning engine
    train.train() # start training

test_train() # starting!
