import Treasure
class Tile:

    def __init__(self,description:str,value:int, treasure:Treasure = None):
        self.description = '.'
    def __str__(self):
        return f'{self.name}({self.treasure})'

