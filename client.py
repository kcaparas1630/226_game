from socket import socket, AF_INET, SOCK_STREAM
from struct import unpack, pack
import struct

connections = {}
PLAYER1 = '4'
PLAYER1_STR = '1'
PLAYER2 = '8'
PLAYER2_STR = '2'
i = 0
def create_client():
    BUF_SIZE = 1024
    HOST = '127.0.0.1'
    PORT = 12345

    with socket(AF_INET, SOCK_STREAM) as sock:
        try:
            global connections
            sock.connect((HOST,PORT))
            sock_name = sock.getsockname()
            print('Client: ', sock.getsockname())
            response = sock.recv(2)
            if response == b'\x00\x01':
                connections[PLAYER1] = sock_name
            if response == b'\x00\x02':
                connections[PLAYER2] = sock_name
            print(connections)
            while True:
                command_bits = b''
                command = input("Enter a command:")
                if command == 'U':
                    if response == b'\x00\x01':
                        command_bits = bytes([0b00100100])
                    elif response == b'\x00\x02':
                        command_bits = bytes([0b00101000])
                elif command == 'L':
                    if response == b'\x00\x01':
                        command_bits = bytes([0b01000100])
                    elif response == b'\x00\x02':
                        command_bits = bytes([0b01001000])
                elif command == 'R':
                    if response == b'\x00\x01':
                        command_bits = bytes([0b01100100])
                    elif response == b'\x00\x02':
                        command_bits = bytes([0b01101000])
                elif command == 'D':
                    if response == b'\x00\x01':
                        command_bits = bytes([0b00110100])
                    elif response == b'\x00\x02':
                        command_bits = bytes([0b00111000])
                elif command == 'Q':
                    command_bits = bytes([0b10000100])
                    break
                else:
                    print("Unknown command")
                    break
                # Send the 1-byte segment to the server
                sock.sendall(command_bits)
                reply = sock.recv(BUF_SIZE)
                # Extract game state information from the received data
                game_state = reply[-1]
                print("Game State:", "Game Over"  if game_state == 1 else "In Progress")
                reply = reply[:-1]  # Remove the game state byte
                # Process the remaining reply data
                print('Reply:', reply)
                if game_state == 1:  # Check if the game is over
                    print("Game Over. Closing the connection.")
                    for c in connections:
                        c.close()
                    break
        except Exception as details:
            print(f'Error: {details}')

if __name__ == '__main__':
    create_client()