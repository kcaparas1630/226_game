from Board import Board
from Treasure import Treasure
from Tile import Tile
from Player import Player
import random


class View:
    def __init__(self,board:Board):
        self.min_val = 0
        self.max_val = 0


