import json

import chess.engine
import coloredlogs

import train
from utils import *

coloredlogs.install(level='INFO')

logger = logging.getLogger("MarcoEngineTraining")
board = chess.Board()


# engine
class Engine:
    def __init__(self, engine_path, weights_filename):
        self.engine = chess.engine.SimpleEngine.popen_uci(str(engine_path))
        self.weights = json.load(open(weights_filename, 'r'))

    def go(self, depth: int = None):
        if depth is None:
            for deep in range(0, 101):
                info = train.analyze(self.engine, board, deep)
                result = train.best_move(self.engine, board, deep)

                if str(board.fen()) in list(self.weights.values()):
                    result = get_key(self.weights, str(result))

                    print_l(f'Uses weight from fen: {board.fen()}')
                    print_l(str(info) + f' | {deep} depth')
                    print_l(str(result))
                    print('\n' * 3)

                else:
                    print_l(str(board.fen()) + ' not in weights! Analyzing without weights...')
                    print_l(str(info) + f' | {deep} depth')
                    print_l(str(result))
                    print('\n' * 3)

            return result


        elif not depth is None:
            print_l(str(list(self.weights.values())) + ' weights loaded!')

            for deep in range(0, depth + 1):
                info = train.analyze(self.engine, board, deep)
                result = train.best_move(self.engine, board, deep)

                if str(board.fen()) in list(self.weights.values()):
                    result = get_key(self.weights, str(result))

                    print_l(f'Uses weight from fen: {board.fen()}')
                    print('\n' * 3)

                else:
                    print_l(str(board.fen()) + ' not in weights! Analyzing without weights...')
                    print('\n' * 3)

                return result

            self.engine.quit()
            return


if __name__ == '__main__':
    engin = Engine("stockfish", "weights/weights_norm.json")
    engin.go(depth=20)
