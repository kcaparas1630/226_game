class Treasure:

    def __init__(self):
        self.description = '$'
        self.value = 0

        def __str__(self):
            return f'{self.value}'