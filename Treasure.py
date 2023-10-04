class Treasure:

    def __init__(self,description:str,value:int):
        self.description = description
        self.value = value

        def __str__(self):
            return f'{self.value}'