from Board import Board
from Treasure import Treasure
import random


class View:
    def __init__(self,board:Board):
        self.min_val = 0
        self.max_val = 0


    def display():
        board = Board(10,5,0,9)
        treasure = Treasure()
        boardPrint = [["." for _ in range(board.n)]for _ in range(board.n)]

        for _ in range(board.t):
            row = random.randint(board.min_val, board.max_val - 1)
            col = random.randint(board.min_val, board.max_val - 1)
            boardPrint[row][col] = treasure.description
        return boardPrint

    result = display()
    for row in result:
        print(''.join(row))