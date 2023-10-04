from Board import Board
from Player import Player

if __name__ == '__main__':

    boardInstance = Board(10, 5, 0, 9, 2)
    boardInstance.add_player("1", 4, 5)
    boardInstance.add_player("2", 5, 5)

    currentPlayer = input("Choose a player: ")  # Initialize with player 1

    while True:
        # Display the board at the beginning of each turn
        boardMap = boardInstance.display()

        for row in boardMap: #creates mapping of the board
            print(' '.join(row))

        while True:
            try:
                playerMovement = input(f"(U)p (L)eft (R)ight (D)own (Q)uit? ")
                boardInstance.move_player(currentPlayer, playerMovement)
                break  #break inner loop if input is valid
            except ValueError as e:
                print(e)  #print the error message //refer to board class

        boardInstance.check_for_treasure()#method call of treasure check
        #compare the players' score
        player1 = boardInstance.players[0]
        player2 = boardInstance.players[1]

        print(f"Player 1 Score: {player1.score}")
        print(f"Player 2 Score: {player2.score}")

        #Check if all treasure has been found
        if not boardInstance.treasurePositions:
            #Compare score to check who won the game.
            if player1.score > player2.score:
                print("Player 1 won!")
            elif player2.score > player1.score:
                print("Player 2 won!")
            else: # if ever it ties that is, but highly doubt it because of random values.
                print("It's a tie!")
            #exit the game
            break
        #CurrentPlayer switch
        if currentPlayer == "2":
            currentPlayer = "1"
        else:
            currentPlayer = "2"
