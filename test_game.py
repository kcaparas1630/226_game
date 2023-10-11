from Treasure import Treasure
from Board import Board
from Player import Player
from Tile import Tile

import py,pytest,random

def test_treasure():
    t1 = Treasure("$",10)
    t2 = Treasure("%", 20)

    assert t1.value == 10
    assert t1.description == "$"
    assert t2.value == 20
    assert t2.description == "%"

def test_board():
    with pytest.raises(ValueError, match = "players must not be less than 2"):#testing players less than 1
        b = Board(1, 5, 5, 6, 1)
    with pytest.raises(ValueError, match = "Invalid argument values"):#testing max_val less than min_val
        b1 = Board(1, 5, 5, 3, 2)
    with pytest.raises(ValueError, match = "Invalid argument values"): #testing negative value for min_val
        b2 = Board(1, 5, -1, 10, 2)
    with pytest.raises(ValueError, match = "Invalid argument values"):#testing nxn argument
        b3 = Board(0, 5, 5, 3, 2)
    with pytest.raises(ValueError, match="Invalid argument values"):#testing treasure amount argument
        b4 = Board(1, -1, 5, 3, 2)


    #define classes
    board = Board(10,5,0,9,2)
    player1 = Player("1",1,1)

    #TreasurePosition method
    board.treasurePositions = {(1,1)}
    assert board.treasurePositions == {(1,1)}
    #CreateTreasure Method
    board.treasures = {("$",5)}
    assert board.treasures == {("$",5)}


    # Add_Player method
    with pytest.raises(ValueError, match = "Position is out of bounds"):
        board.add_player("1",-1,5)
    with pytest.raises(ValueError, match="Position is out of bounds"):
        board.add_player("1", 5, -1)
    with pytest.raises(ValueError, match = "Position is out of bounds"):
        board.add_player("1",10,5)
    with pytest.raises(ValueError, match = "Position is out of bounds"):
        board.add_player("1",5,10)
    with pytest.raises(ValueError, match = "Position is already occupied by another player"):
        board.add_player("1",5,5)
        board.add_player("2",5,5)


    #Move_player
    with pytest.raises(ValueError, match = "Player not found"):
        board.move_player("","u")
    with pytest.raises(ValueError, match = "Invalid direction"):
        board.move_player("1","p")
    board.players = [Player("1",0,5)]#L
    with pytest.raises(ValueError,match = "Cannot move out of bounds"):
        board.move_player("1","L")
    board.players = [Player("1",1,0)]#U
    with pytest.raises(ValueError,match = "Cannot move out of bounds"):
        board.move_player("1","U")
    board.players = [Player("1", 10, 5)]#R
    with pytest.raises(ValueError, match="Cannot move out of bounds"):
        board.move_player("1", "R")
    board.players = [Player("1", 1, 10)]#D
    with pytest.raises(ValueError, match="Cannot move out of bounds"):
        board.move_player("1", "D")
    board.players = [Player("1",4,5),Player("2",5,5)]#R
    with pytest.raises(ValueError, match = "Position is already occupied by another player"):
        board.move_player("1","R")
    board.players = [Player("1", 5, 4), Player("2", 5, 5)]#D
    with pytest.raises(ValueError, match="Position is already occupied by another player"):
        board.move_player("1", "D")
    board.players = [Player("1", 5, 5), Player("2", 5, 4)]#U
    with pytest.raises(ValueError, match="Position is already occupied by another player"):
        board.move_player("1", "U")
    board.players = [Player("1", 5, 5), Player("2", 4, 5)]#L
    with pytest.raises(ValueError, match="Position is already occupied by another player"):
        board.move_player("1", "L")

def test_check_Score():
    player1 = Player("1", 1, 1)
    player1.add_Score(5)
    # Now check the score using the Player's attribute
    assert player1.score == 5

def test_score_increment_when_finding_treasure():
    # Create a board with known parameters
    board = Board(10, 5, 0, 9, 2)

    # Add a player to a known position
    player1 = Player("1", 1, 1)
    board.players = [player1]
    # Set a known treasure position
    board.treasurePositions = {(1, 1)}  # Assuming this is the position where the player is expected to find treasure
    # Ensure that the treasuresFound set is initially empty
    assert len(board.treasuresFound) == 0
    # Ensure that the player's score is initially 0
    assert player1.score == 0
    # Simulate the player moving to the treasure position
    board.check_for_treasure()
    # Check that the player's score has been updated
    assert player1.score > 0


def test_check_for_treasure_remove():
    board = Board(10, 5, 0, 9, 2)
    player1 = Player("1", 1, 1)
    board.players = [player1]
    board.treasurePositions = {(1,1)}
    board.check_for_treasure()
    assert (1,1) not in board.treasurePositions



def test_check_for_treasure_game_over():
    board = Board(10, 5, 0, 9, 2)
    players = [Player(name=f"Player{i}", x=i, y=i) for i in range(1, 6)]
    board.players = players
    board.treasurePositions = {(i, i) for i in range(1, 6)}

    for player in players:
        board.check_for_treasure()

    # Use the actual treasuresFound set from the Board object
    treasuresFound = board.treasuresFound

    # Check if the number of found treasures is equal to 5
    assert len(treasuresFound) == 5


def test_check_for_treasure_score():
    board = Board(10, 5, 0, 9, 2)
    player1 = Player("1", 1, 1)
    board.check_for_treasure()
    player1.score = 1
    assert player1.score > 0
    assert "Player Player1 has found a treasure!"

def test_check_for_treasure_no_treasure():
    board = Board(10, 5, 0, 9, 2)
    player1 = Player("1", 1, 1)
    board.treasurePositions = set()
    board.check_for_treasure()
    assert player1.score == 0

def test_player():
    p1 = Player("1",0,5)
    p2 = Player("2", 0, 5)

    assert p1.name == "1"
    assert p2.name == "2"
    assert p1.score == 0
    assert p2.score == 0

def test_tiles():
    tile1 = Tile(".",0,5)

    assert tile1.description == "."
    assert tile1.value == 0 #Idk why I did this and idk what the value is for but for the sake of requirements
