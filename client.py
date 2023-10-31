from socket import socket, AF_INET, SOCK_STREAM
from struct import unpack, pack
import struct


def create_client():
    BUF_SIZE = 1024
    HOST = '127.0.0.1'
    PORT = 12345

    with socket(AF_INET, SOCK_STREAM) as sock:
        try:
            sock.connect((HOST,PORT))
            print('Client: ', sock.getsockname())
            response = sock.recv(2)
            if response == b'\x00\x03':
                print("Connection refused by the server.")
                return
            print(response)
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
                print(reply)


        except BrokenPipeError as details:
            print(f'Error: {details}')
        except ConnectionRefusedError as details:
            print(f'Error: {details}')

if __name__ == '__main__':
    create_client()
