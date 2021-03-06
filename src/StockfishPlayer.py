from stockfish import Stockfish

class StockfishPlayer:
    def __init__(self, stockfishpath):
        conf = {
            "Write Debug Log": "false",
            "Contempt": 0,
            "Min Split Depth": 0,
            "Threads": 1,
            "Ponder": "false",
            "Hash": 16,
            "MultiPV": 1,
            "Skill Level": 20,
            "Move Overhead": 30,
            "Minimum Thinking Time": 20,
            "Slow Mover": 80,
            "UCI_Chess960": "false",
        }
        self.stockfish = Stockfish(stockfishpath, parameters=conf)

    def get_best_move(self, fen):
        self.stockfish.set_fen_position(fen)
        return self.stockfish.get_best_move()

    