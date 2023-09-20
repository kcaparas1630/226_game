import Treasure, Tile, random

class Board:

    def __init__(self,n,t, min_val:int,max_val:int):
        #Check that variables are numeric, not negative, and max_val not less than minimum

        if n <= 0 or t < 0 or min_val < 0 or max_val <= min_val:
            raise ValueError("Invalid argument values.")

        self.n = n
        self.t = t
        self.min_val = min_val
        self.max_val = 10

    #treasure = random.randint(min_val,max_val) treasure works like this
