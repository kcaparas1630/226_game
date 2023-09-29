import Treasure, Player
class Tile:

    def __init__(self,description:str,value:int, treasure:Treasure = None):
        self.description = '.'
        self.value = value
    def __str__(self):
        return f'{self.description}({self.treasure})'
