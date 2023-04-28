from gomoku_hack.board import Board


def main():
    board = Board()
    
    stones = [
        [1, 0, True], 
        [2, 0, True], 
        [3, 0, False], 
    ]
    for s in stones:
        board.update(*s)
    
    board.show()
    
    print(1)


if __name__ == "__main__":
    main()