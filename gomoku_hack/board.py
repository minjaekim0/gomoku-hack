from typing import List, Union
import numpy as np


class Board:
    def __init__(self) -> None:
        self.board_len = 15
        self.blank = "  "
        self.black_stone = "🟤"
        self.white_stone = "⚪️"
        self.board = [[self.blank for _ in range(self.board_len)] for _ in range(self.board_len)]
        self.board_calc = np.full((self.board_len, self.board_len), np.nan)
    
    def update(self, x: int, y: int, is_black: bool) -> None:
        r = 7 - y
        c = x + 7
        if is_black:
            self.board[r][c] = self.black_stone
            self.board_calc[r, c] = 1
        else:
            self.board[r][c] = self.white_stone
            self.board_calc[r, c] = 0
        
        vc = VictoryChecker(self.board_calc)
        victory = vc.check()
        if victory == "black":
            print("black win.")
        elif victory == "white":
            print("white win.")
    
    def str_for_show(self) -> str:
        first_row = "   ┌" + "────┬" * (self.board_len - 1) + "────┐\n"
        divide_row = "   ├" + "────┼" * (self.board_len - 1) + "────┤\n"
        last_row = "   └" + "────┴" * (self.board_len - 1) + "────┘\n"
        
        output = ""
        output += first_row
        for r in range(self.board_len):
            output += f"{7-r:+2d} "
            for c in range(self.board_len):
                output += f"│ {self.board[r][c]} "
            output += "│\n"
            
            if r < self.board_len - 1:
                output += divide_row
            
        output += last_row
        output += "  "
        for c in range(self.board_len):
            output += f"   {c-7:+2d}"
        return output
    
    def show(self) -> None:
        print(self.str_for_show())


class VictoryChecker:
    def __init__(self, board_calc: List[List[Union[int, None]]]) -> None:
        self.board_len = 15
        self.board_calc = board_calc
    
    def check(self) -> str:
        result_h = self._check_horizontal(self.board_calc)
        result_v = self._check_vertical(self.board_calc)
        result_dd = self._check_diagonal_downward(self.board_calc)
        result_du = self._check_diagonal_upward(self.board_calc)
        
        if result_h in ("black", "white"):
            return result_h
        elif result_v in ("black", "white"):
            return result_v
        elif result_dd in ("black", "white"):
            return result_dd
        elif result_du in ("black", "white"):
            return result_du
        else:
            return "no"
    
    def _check_horizontal(self, board_calc) -> str:
        for r in range(self.board_len):
            for c in range(self.board_len - 4):
                subject = board_calc[r, c:c+5]
                if np.array_equal(subject, [1] * 5):
                    return "black"
                elif np.array_equal(subject, [0] * 5):
                    return "white"
        return "no"
    
    def _check_vertical(self, board_calc) -> str:
        transposed = board_calc.T
        return self._check_horizontal(transposed)
        
    def _check_diagonal_downward(self, board_calc) -> str:
        for r in range(self.board_len - 4):
            for c in range(self.board_len - 4):
                subject = board_calc[r:r+5, c:c+5].diagonal()
                if np.array_equal(subject, [1] * 5):
                    return "black"
                elif np.array_equal(subject, [0] * 5):
                    return "white"
        return "no"
    
    def _check_diagonal_upward(self, board_calc) -> str:
        flipped = np.flipud(board_calc)
        return self._check_diagonal_downward(flipped)
