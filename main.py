"""from Board import Board
from Player import Player

if __name__ == '__main__':

    boardInstance = Board(10, 5, 0, 9, 2)
    boardInstance.add_player("1", 4, 5)
    boardInstance.add_player("2", 5, 5)

    while True:

        # Display the board at the beginning of each turn
        boardMap = boardInstance.display()

        for row in boardMap: #creates mapping of the board
            print(' '.join(row))
        currentPlayer = input("Choose a player: ")  # Initialize with player 1
        while True:
            try:
                playerMovement = input(f"Player {currentPlayer} (U)p (L)eft (R)ight (D)own (Q)uit? ")
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
"""
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from sys import argv
from Board import Board

class Game:
    def __init__(self):
        self.board_instance = Board(10, 5, 0, 9, 2)
        self.board_instance.add_player("1", 4, 5)
        self.board_instance.add_player("2", 5, 5)
        self.command_mapping = {'U': 0b0010, 'L': 0b0100, 'R': 0b0110, 'D': 0b0011, 'Q': 0b1000, 'G': 0b1111}


    def create_server(self):
        BUF_SIZE = 1024
        HOST = '127.0.0.1'
        PORT = 12345

        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
            sock.bind((HOST,PORT))
            sock.listen(1)
            print('Server: ', sock.getsockname())
            while True:
                try:
                    sc, address = sock.accept()
                    with sc:
                        client_ip, client_port = address
                        print('Client connected:', address)

                        # Receive 1-byte segment
                        data = sc.recv(1)

                        if not data:
                            print('Client disconnected:', address)
                            break

                        # Decode the command, player number, and unused bits
                        commands = (data[0] & 0xF0) >> 4

                        player_number = (data[0] & 0x0C) >> 2
                        """
                        unused_bits = data[0] & 0x03

                        if unused_bits != 0:
                            print('Invalid command. Closing connection.')
                            break
                        """

                        print(f'Received: Command={commands}, Player={player_number}')

                        str_player_number = str(player_number)
                        str_commands = next(key for key, value in self.command_mapping.items() if value == commands)
                        # Handle different commands
                        print(f'commands before  {commands}')
                        if commands == 0b0010:  # U
                            print('Player pos before: %d, %d' % (self.board_instance.players[0].x, self.board_instance.players[0].y))
                            self.board_instance.move_player(str_player_number, str_commands)
                            print('Player pos after: %d, %d' % (self.board_instance.players[0].x, self.board_instance.players[0].y))
                            pass
                        elif commands == 0b0100:  # L
                            # Handle L command
                            print('Player pos before: %d, %d' % (
                            self.board_instance.players[0].x, self.board_instance.players[0].y))
                            self.board_instance.move_player(str_player_number, str_commands)
                            print('Player pos after: %d, %d' % (
                            self.board_instance.players[0].x, self.board_instance.players[0].y))
                            pass
                        elif commands == 0b0110:  # R
                            # Handle R command
                            print('Player pos before: %d, %d' % (
                            self.board_instance.players[0].x, self.board_instance.players[0].y))
                            self.board_instance.move_player(str_player_number, str_commands)
                            print('Player pos after: %d, %d' % (
                            self.board_instance.players[0].x, self.board_instance.players[0].y))
                            pass
                        elif commands == 0b0011:  # D
                            # Handle D command
                            print('Player pos before: %d, %d' % (
                            self.board_instance.players[0].x, self.board_instance.players[0].y))
                            self.board_instance.move_player(str_player_number, str_commands)
                            print('Player pos after: %d, %d' % (
                            self.board_instance.players[0].x, self.board_instance.players[0].y))
                            pass
                        elif commands == 0b1000:  # Q
                            # Handle Q command
                            pass
                        elif commands == 0b1111:  # G
                            # Handle G command
                            boardMap = self.board_instance.display()
                            for row in boardMap:  # creates mapping of the board
                                print(' '.join(row))
                            pass
                        else:
                            print('Unknown command. Closing connection.')
                            break
                        self.check_treasures()

                except Exception as details:
                    raise details

    def create_client(self,command):
        BUF_SIZE = 1024
        HOST = '127.0.0.1'
        PORT = 12345

        with socket(AF_INET,SOCK_STREAM) as sock:
            try:
                sock.connect((HOST,PORT))
                print('Client: ', sock.getsockname())
                #player_number &= 0b01

                # Create the 1-byte segment
                #byte_segment = ((self.command_mapping[command] & 0xF0) | (player_number << 2)).to_bytes(1,byteorder='big')
                commandBits = b''
                if command == 'G':
                    commandBits = bytes([0b11110100])
                elif command == 'U':
                    player_number = int(input("Enter which player to move: "))
                    if player_number == 1:
                        commandBits = bytes([0b00100100])
                    elif player_number == 2:
                        commandBits = bytes([0b00101000])
                    else:
                        print("No player exists")
                elif command == 'L':
                    player_number = int(input("Enter which player to move: "))
                    if player_number == 1:
                        commandBits = bytes([0b01000100])
                    elif player_number == 2:
                        commandBits = bytes([0b01001000])
                    else:
                        print("No player exists")
                elif command == 'R':
                    player_number = int(input("Enter which player to move: "))
                    if player_number == 1:
                        commandBits = bytes([0b01100100])
                    elif player_number == 2:
                        commandBits = bytes([0b01101000])
                    else:
                        print("No player exists")
                elif command == 'D':
                    player_number = int(input("Enter which player to move: "))
                    if player_number == 1:
                        commandBits = bytes([0b00110100])
                    elif player_number == 2:
                        commandBits = bytes([0b00111000])
                    else:
                        print("No player exists")
                elif command == 'Q':
                    commmandBits = bytes([0b10000100])
                # Send the 1-byte segment to the server
                sock.sendall(commandBits)
                reply = sock.recv(BUF_SIZE)
                print('Reply: ', reply)
            except Exception as details:
                raise details
                #print(f'Error: {details}')
            finally:
                sock.close()

    def check_treasures(self):
        self.board_instance.check_for_treasure()
        player1 = self.board_instance.players[0]
        player2 = self.board_instance.players[1]

        print(f"Player 1 Score: {player1.score}")
        print(f"Player 2 Score: {player2.score}")

        # Check if all treasure has been found
        if not self.board_instance.treasurePositions:
            # Compare score to check who won the game.
            if player1.score > player2.score:
                print("Player 1 won!")
            elif player2.score > player1.score:
                print("Player 2 won!")
            else:  # if ever it ties that is, but highly doubt it because of random values.
                print("It's a tie!")


if __name__ == '__main__':
    g = Game()



    if len(argv) < 2:
        print(f'Usage: {argv[0]} + <command>')
        exit()

        # Assuming argv[1] is the command (e.g., 'U', 'L', 'R', 'D', 'Q', 'G')
    command = argv[1]
    #player_number = int(input("Enter player number (1 or 2): "))
    # Run either the server or the client based on the command
    if command.lower() == 'server':
        g.create_server()

    else:
        g.create_client(command)
