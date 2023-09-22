from Board import Board
from Treasure import Treasure
from Tile import Tile
from Player import Player
import random


class View:
    def __init__(self,board:Board):
        self.min_val = 0
        self.max_val = 0


    def display(): #Method where the 2d view is made
        board = Board(10,5,0,9 , 1)
        treasure = Treasure()
        tile = Tile(".", 0,5)
        player = Player("1")
        boardPrint = [[tile.description for _ in range(board.n)]for _ in range(board.n)]#Created a 2d array using nxn collection

        for _ in range(board.t): #used random to create random appearance of treasure.
            row = random.randint(board.min_val, board.max_val - 1)
            col = random.randint(board.min_val, board.max_val - 1)
            boardPrint[row][col] = treasure.description #assigned boardPrint array with '$'
        for _ in range(board.max_players): #used random to create random appearance of treasure.
            row = random.randint(board.min_val, board.max_val - 1)
            col = random.randint(board.min_val, board.max_val - 1)
            boardPrint[row][col] = player.name #assigned boardPrint array with '$'
        return boardPrint

    result = display() #Assigned result with boardPrint array
    for row in result: #Mapping the view
        print(' '.join(row))