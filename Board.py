import random, sys
from Player import Player
from Treasure import Treasure
from Tile import Tile


class Board:

    def __init__(self, n, t, min_val: int, max_val: int, max_players: int):
        # Check that variables are numeric, not negative, and max_val not less than minimum
        if n <= 0 or t < 0 or min_val < 0 or max_val <= min_val:
            raise ValueError("Invalid argument values.")
        # Check that maximum players is not negative nor greater than n
        if max_players < 2:
            raise ValueError("players must not be less than 2")

        self.max_players = max_players
        self.n = n
        self.t = t
        self.min_val = min_val
        self.max_val = max_val
        self.players = []
        self.treasures = self.create_treasures()  # instance method inside init
        self.treasurePositions = self.create_treasure_positions()  # instance method inside init
        self.tile = Tile(".", 0, t)
        self.treasuresFound = set()  # Create a set to store found treasures

    def create_treasures(self):  # method to generate treasure class returns an list called treasures
        treasures = []
        for _ in range(self.t):
            description = '$'
            value = random.randint(5, 10)  # Assign value of 5 - 10 for value of treasures
            treasures.append(Treasure(description, value))  # Insert values to treasure class
        return treasures

    def create_treasure_positions(
            self):  # method to generate random position of treasures return a set collection of treasures
        treasurePositions = set()
        while len(
                treasurePositions) < self.t:  # Will continue to loop while treasure.positions is less than treasures (5)
            row = random.randint(self.min_val, self.max_val - 1)  # row with range of min-val and max-val - 1
            col = random.randint(self.min_val, self.max_val - 1)  # col with range of min-val and max-val - 1
            treasurePositions.add((row, col))
        return treasurePositions

    def add_player(self, name, x, y):  # method to add player accepts parameters name, and x, y coordinates. Void return
        if (x < 0) or (y < 0) or (x >= self.n) or (y >= self.n):  # condition to check if x or y coordinate is less than or equal to 0  or greater than 10
            raise ValueError("Position is out of bounds")

        for player in self.players:  # self.players is an array created in the init method
            if player.x == x and player.y == y:  # condition to check if coordinates is same as other player.
                raise ValueError("Position is already occupied by another player")

        new_player = Player(name, x, y)  # instance method of player class
        self.players.append(new_player)  # append player instance to self.players array

    def move_player(self, name,
                    direction):  # Method to move player accepts parameters name, and direction(up, down, right, left)
        movePlayer = None  # initializing variable to none for looping

        # Find the player with the given name
        for player in self.players:
            if player.name == name:
                movePlayer = player
                break

        if movePlayer is None:  # check if player is none and not assigned earlier in the loop
            raise ValueError("Player not found")

        x, y = movePlayer.x, movePlayer.y

        # Define the new position based on the direction
        if (direction == "U") or (direction == "u"):
            new_x, new_y = x, y - 1
        elif (direction == "D") or (direction == "d"):
            new_x, new_y = x, y + 1
        elif (direction == "L") or (direction == "l"):
            new_x, new_y = x - 1, y
        elif (direction == "R") or (direction == "r"):
            new_x, new_y = x + 1, y
        elif (direction == "Q") or (direction == "q"):
            sys.exit(1)  # force terminates the program
        else:
            raise ValueError("Invalid direction")

        # Check if the new position is out of bounds
        if (new_x < 0) or (new_y < 0) or (new_x >= self.n) or (new_y >= self.n):
            raise ValueError("Cannot move out of bounds")

        # Check if the new position is already occupied by another player
        for player in self.players:
            if player.x == new_x and player.y == new_y:
                raise ValueError("Position is already occupied by another player")

        # Update the player's position
        movePlayer.x, movePlayer.y = new_x, new_y

    def display(
            self):  # method where it prints the board. returns board list of string of board P.S. NEEDS TO BE IMPLEMENTED TO VIEW CLASS
        treasures = self.create_treasures()  # created an instance method of generate_treasures
        treasureDesc = treasures[0]  # called to get description of treasures "$"
        boardPrint = [[self.tile.description for _ in range(self.n)] for _ in
                      range(self.n)]  # created list of array to create the tile board

        for row, col in self.treasurePositions:  # assign treasures randomly in the board
            boardPrint[row][col] = treasureDesc.description
        for player in self.players:  # Assigns the player
            x, y = player.x, player.y
            boardPrint[y][x] = player.name  # Set the player's position

        return boardPrint

    def check_for_treasure(self):
        #treasuresFound = set()  # Create a set to store found treasures
        treasures = self.create_treasures()
        treasuresVal = treasures[0]  # variable initialized to get value of treausre.
        treasure_positions_copy = self.treasurePositions.copy()
        treasuresToRemove = set()  # Create a set to store treasures to be removed

        for player in self.players:
            x, y = player.x, player.y

            for row, col in treasure_positions_copy:
                if x == col and y == row:
                    # Player found treasure at the same coordinates
                    player.score += treasuresVal.value
                    self.treasuresFound.add((row, col))  # Add the found treasure to the set
                    # Print the player's name and updated score
                    print(f"Player {player.name} has found a treasure! Score: {player.score}")
                    treasuresToRemove.add((row, col))  # Add the treasure to the removal set

        # Remove the found treasures from the main set
        for treasure in treasuresToRemove:
            self.treasurePositions.remove(treasure)
        if (len(self.treasuresFound) == 5):
            print(f"Game is over")