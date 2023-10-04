

class Player:
        def __init__(self,name,x,y):
            self.name = name;
            self.score = 0;
            self.x = x;
            self.y = y;
        def __str__(self):
            return f'{self.name}:{self.score}'
        def add_Player(self, name,x,y):
            return f'{self.name}'
        def add_Score(self,name,score):
            return f'{self.name}:{self.score}'
