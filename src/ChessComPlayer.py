from BoardAPI import BoardAPI
from StockfishPlayer import StockfishPlayer
import time

class ChessComPlayer:
    def __init__(self, top_right, lenght, playing_color, stockfishpath):
        self.board = BoardAPI(top_right, lenght, playing_color)
        self.stockfishplayer = StockfishPlayer(stockfishpath)

    def make_best_move(self):
        fen = self.board.get_board_state_fen()
        print(f"make_best_move: fen {fen}")
        #best_move = self.stockfishplayer.get_best_move(fen)
        self.stockfishplayer.stockfish.set_fen_position(fen)
        best_move = self.stockfishplayer.stockfish.get_best_move_time(5000)
        print(f"make_best_move: best move {best_move}")

        self.board.move_figure_from_to(best_move)

        print("make_best_move: \n ")
        print(self.board.board)

    def is_my_turn(self):
        print(f"is my turn: board state: {self.board.get_board_state_fen()}")
        return self.board.is_my_turn()

    def after_rivals_move(self):
        self.board.update_board_after_rival_move()

        print("after rivals move: \n ")
        print(self.board.board)


if __name__ == "__main__" : 
    color = "black"
    player = ChessComPlayer(
        (270,171),
        760, color,
        r"C:\Users\Superuser\PythonProjects\ChessNerdsDestroyer\stockfish\stockfish.exe")
    time.sleep(3)
    if (color == "white"):
        player.make_best_move()
    else : 
        player.after_rivals_move()

    while True:
        time.sleep(3)
        if player.is_my_turn():
            player.make_best_move()
        else:
            player.after_rivals_move()
