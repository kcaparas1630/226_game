import threading
from threading import Semaphore,Thread
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from sys import argv
import struct
import client



from Board import Board

class Game:

    def __init__(self,host, port):
        self.board_instance = Board(10, 5, 0, 9, 2)
        self.board_instance.add_player("1", 0, 1)
        self.board_instance.add_player("2", 9,1)
        self.command_mapping = {'U': 0b0010, 'L': 0b0100, 'R': 0b0110, 'D': 0b0011, 'Q': 0b1000, 'G': 0b1111}
        self.host = host
        self.port = port
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        self.sock.bind((self.host,self.port))

    def listen(self):
        self.sock.listen(1)
        containers = [0, 0]
        thread_list = []
        print("Server: ", self.sock.getsockname())
        while True:
            sc, address = self.sock.accept()
            if len(containers) > 3:
                print("Exceeded Players")
                sc.close()
                continue  # Skip the rest of the loop and continue accepting connections
            for i in range(1, 3):
                if i not in containers:
                    containers.append(i)
                    response = struct.pack('!H', i)  # Convert the client number to bytes
                    sc.send(response)
                    break
            thread = threading.Thread(target=self.listenToClient, args=(sc, address,containers))
            thread_list.append(thread)
            thread.start()
        for t in thread_list:
            t.join()

    def listenToClient(self, sc, address,containers):
        BUF_SIZE = 1024
        try:
            while True:
                print('Client connected:', sc.getpeername())
                data = sc.recv(BUF_SIZE)
                if not data:
                    print("Client Disconnected")
                    sc.close()
                    break
                self.playCommand(sc, data)
        except Exception as details:
            print(f'Error: {details}')
            sc.close()

    def getBoard(self):
        boardMap = self.board_instance.display()
        for row in boardMap:  # creates mapping of the board
            print(' '.join(row))
            # Check for treasures
        self.board_instance.check_for_treasure()
        # Print player scores
        player1 = self.board_instance.players[0]
        player2 = self.board_instance.players[1]
        print(f"Player 1 Score: {player1.score}")
        print(f"Player 2 Score: {player2.score}")
        # Convert the boardMap to a UTF-8 encoded string
        board_str = '\n'.join([' '.join(row) for row in boardMap])
        board_bytes = board_str.encode('utf-8')
        headers = struct.pack('!H', len(board_bytes))
        # Pack Player 1 and Player 2 scores as unsigned shorts
        player_score = struct.pack('!HH', player1.score, player2.score)
        game_state = struct.pack('!B', 1 if self.board_instance.game_over else 0)
        print(game_state)
        header_length = len(board_bytes) + len(player_score)
        header_bytes = struct.pack('!H',header_length)
        return header_bytes + player_score + board_bytes + game_state

    """def check_for_win(self):
        player1 = self.board_instance.players[0]
        player2= self.board_instance.players[1]
        player_win = ''
        if player1.score > player2.score:
            print("PLAYER 1 WIN!")
            player_win = player1
        elif player2.score > player1.score:
            print("PLAYER 2 WIN!")
            player_win = player2
        player_win_info = player_win.name  # Replace 'name' with the actual attribute of the Player object you want to send
        player_win_bytes = player_win_info.encode('utf-8')
        return player_win_bytes"""

    def playCommand(self,sc,data):
        commands = (data[0] & 0xF0) >> 4
        player_number = (data[0] & 0x0C) >> 2
        lock = Semaphore()

        print(f'Received: Command={commands}, Player={player_number}')
        str_player_number = str(player_number)
        str_commands = next(key for key, value in self.command_mapping.items() if value == commands)

        # Handle different commands
        if commands == 0b0010:  # U
            with lock:
                self.board_instance.move_player(str_player_number, str_commands)
                print(len(self.board_instance.treasuresFound))
                sc.sendall(self.getBoard())
        elif commands == 0b0100:  # L
            # Handle L command
            with lock:
                self.board_instance.move_player(str_player_number, str_commands)

                sc.sendall(self.getBoard())
        elif commands == 0b0110:  # R
            # Handle R command
            with lock:
                self.board_instance.move_player(str_player_number, str_commands)
                sc.sendall(self.getBoard())
        elif commands == 0b0011:  # D
            # Handle D command
            with lock:
                self.board_instance.move_player(str_player_number, str_commands)
                sc.sendall(self.getBoard())
        elif commands == 0b1111: #G
            with lock:
                sc.sendall(self.getBoard())
        elif commands == 0b1000:  # Q
            print("Thanks for playing!")
            sc.close()  # Close the connection
        else:
            print('Unknown command. Closing connection.')
            sc.close()




if __name__ == '__main__':
    Game('',12345).listen()
