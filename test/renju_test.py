import sys, os
sys.path.append(os.path.abspath("."))
from gomoku_hack.board import Board
from gomoku_hack.renju import Two4Checker, TwoOpen3Checker, MoreThan6Checker, RenjuChecker


def two_4():
    board = Board()
    
    stones = [
        [-3, 0, True], 
        [-1, 0, True], 
        [1, 0, True], 
        [2, 0, True], 
        [1, 1, True], 
        [2, 2, True], 
        [3, 3, True], 
        [7, 2, True], 
        [7, 3, True], 
        [7, 4, True], 
        [6, 5, True], 
        [5, 4, True], 
        [3, 2, True], 
        [-7, -6, True], 
        [-7, -5, True], 
        [-7, -4, True], 
        [-5, -6, True], 
        [-5, -5, True], 
        [-5, -4, True], 
        [-6, -7, True], 
        [-4, -7, True], 
        [-3, -7, True], 
    ]
    for s in stones:
        board.update(*s)
    
    board.show()
    
    t4c = Two4Checker(board.board_calc)
    for x in range(-7, 8):
        for y in range(-7, 8):
            if t4c.check_two_4(x, y):
                print(x, y)
    
    return


def two_open3():
    board = Board()
    
    stones = [
        [1, 0, True], 
        [2, 0, True], 
        [1, 1, True], 
        [2, 2, True], 
        [3, 1, True], 
        [7, 3, True], 
        [7, 4, True], 
        [6, 5, True], 
        [5, 4, True], 
        [-7, -6, True], 
        [-7, -5, True], 
        [-6, -7, True], 
        [-4, -7, True], 
        [2, 1, False], 
    ]
    for s in stones:
        board.update(*s)
    
    board.show()
    
    t3c = TwoOpen3Checker(board.board_calc)
    for x in range(-7, 8):
        for y in range(-7, 8):
            if t3c.check_two_open3(x, y):
                print(x, y)
    
    return


def more_than_6():
    board = Board()
    
    stones = [
        [1, 0, True], 
        [2, 1, True], 
        [4, 3, True], 
        [5, 4, True], 
        [6, 5, True], 
        [2, 0, True], 
        [-1, 0, True], 
        [-2, 0, True], 
        [-3, 0, True], 
        [-4, 0, True], 
        [-5, 0, True], 
        [2, -1, True], 
        [2, -2, True], 
        [2, -3, True], 
        [2, -4, False], 
        [-6, 7, True], 
        [-5, 7, True], 
        [-4, 7, True], 
        [-3, 7, True], 
        [-2, 7, True], 
    ]
    for s in stones:
        board.update(*s)
    
    board.show()
    
    m6c = MoreThan6Checker(board.board_calc)
    for x in range(-7, 8):
        for y in range(-7, 8):
            if m6c.check_more_than_6(x, y):
                print(x, y)
    
    return


def renju_all_test():
    board = Board()
    
    """
    https://namu.wiki/jump/t98s4gfFdlMtyIH%2BR4cfI30YxxROR0TaYXDJ7VaI5hwhK1aBAoeOVonppNdg%2Fw2k
    
    실제 금수 리스트: (-5, 5), (-5, 0), (-2, 4), (2, 2), (1, 0), (0, -3)
    정답: (-5, 5), (1, 0), (0, -3)
    오답
    - 금수가 맞는데 아니라고 함: (-5, 0), (-2, 4), (2, 2)
    - 금수가 아닌데 맞다고 함: (-3, -5), (-3, -4), (-2, -2), (-1, -2), (-1, -1)
    """
    
    stones = [
        [3, 10, True], 
        [3, 11, True], 
        [3, 12, True], 
        [3, 14, True], 
        [3, 15, True], 
        [4, 12, True], 
        [7, 12, True], 
        [9, 12, True], 
        [10, 12, True], 
        [10, 9, True], 
        [10, 8, True], 
        [10, 6, True], 
        [11, 8, True], 
        [8, 8, True], 
        [8, 7, True], 
        [8, 6, True], 
        [5, 6, True], 
        [5, 5, True], 
        [6, 5, True], 
        [7, 5, True], 
        [7, 4, True], 
        [4, 5, False], 
        [8, 9, False], 
    ]
    for s in stones:
        board.update(*s)
    
    board.show()
    
    rc = RenjuChecker(board.board_calc)
    for x in range(-7, 8):
        for y in range(-7, 8):
            if rc.check(x, y):
                print(x, y)
    
    return


if __name__ == "__main__":
    # two_4()
    # two_open3()
    # more_than_6()
    renju_all_test()
    