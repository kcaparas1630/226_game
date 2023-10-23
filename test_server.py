
from re import compile
from socket import socket, AF_INET, SOCK_STREAM
from struct import unpack
from subprocess import run
from time import sleep
import pytest

#
# DO NOT CHANGE THE CODE BELOW
#


BUF_SIZE = 1024
HOST = '127.0.0.1'
PORT = 12345

PLAYER1 = '4'
PLAYER1_STR = '1'
PLAYER2 = '8'
PLAYER2_STR = '2'

first_run = True


#
#  CONNECTION CODE
#


def get_data(client: socket) -> bytes:
    buffer = b''
    size = 0
    print('Client', client.getsockname(), 'waiting for data')
    while size < BUF_SIZE:
        data = client.recv(1)
        size += 1
        if data == b'':
            print('Client', client.getsockname(), 'received',  buffer.hex(), '(', buffer, ')')
            return buffer
        buffer = buffer + data

    return buffer


def put_data(data: str) -> bytes:
    client = socket(AF_INET, SOCK_STREAM)
    client.connect((HOST, PORT))
    encoded_data = bytes.fromhex(data)
    print('Client', client.getsockname(), 'sending', data, '(', encoded_data.hex(), ')')
    client.sendall(encoded_data)
    response = get_data(client)
    client.close()
    return response


#
#  CONTAINER CODE
#


def start_container():
    print('Attempting to start container.')
    cmd = run(['sudo', 'docker', 'start', '226-server'], capture_output=True)
    print(cmd)


def stop_container():
    print('Attempting to stop container.  This may fail, but that\'s probably ok!')
    cmd = run(['sudo', 'docker', 'stop', '226-server'], capture_output=True)
    print(cmd)


def remove_container():
    print('Attempting to remove container.  This may fail, but that\'s probably ok!')
    cmd = run(['sudo', 'docker', 'rm', '226-server'], capture_output=True)
    print(cmd)


def wait(s):
    for i in range(s):
        print('.', end='')
        sleep(1)
    print()


def setup_module(module):
    stop_container()
    remove_container()

    print('Attempting to build container.')
    cmd = run(['sudo', 'docker', 'build', '-t', '226-server', '.'], capture_output=True)
    print(cmd)

    print('Attempting to run container.')
    cmd = run(['sudo', 'docker', 'run', '-d', '--log-driver', 'journald', '--name', '226-server', '-p', str(PORT) +
               ':' + str(PORT), '-v', '/dev/log:/dev/log', '226-server'], capture_output=True)
    print(cmd)

    wait(5)  # Ugly; should properly detect when the container is up and running


def teardown_module(module):
    print('\n\n')
    stop_container()
    remove_container()


@pytest.fixture(autouse=True)
def restart_container():
    global first_run

    print('\n--------------------------------------------------------------------------------')
    if first_run:
        first_run = False
    else:
        stop_container()
        start_container()
        wait(5) # Ugly; should properly detect when the container is up and running


#
#  TEST CODE
#


def remove_blanks(lst: [str]) -> [str]:
    new_lst = []
    for item in lst:
        if item != '':
            new_lst.append(item)
    return new_lst


def parse_board(board_str: str) -> [[str]]:
    print(board_str)
    nl_pat = compile(r'\n+')
    rows = remove_blanks(nl_pat.split(board_str))
    ws_pat = compile(r' +')
    board = []
    for cols in rows:
        cells = remove_blanks(ws_pat.split(cols))
        board.append(cells)
    return board


def get_scores(result: bytes) -> (int, int):
    score1 = unpack('!H', result[0:2])[0]
    score2 = unpack('!H', result[2:4])[0]
    return score1, score2


def get_board() -> ([[str]], int, int):
    result = put_data('F0')
    score1, score2 = get_scores(result)
    print("The score is",score1)
    assert 0 <= score1 <= 100
    assert 0 <= score2 <= 100
    board = parse_board(result[4:].decode())
    return board, score1, score2


def find_player(player: str, n: int, board: [[str]]) -> (int, int):
    for i in range(n):
        for j in range(n):
            if player in board[i][j]:
                return i, j

    return -1, -1


def move_right_and_up(player: str, player_str: str, score1: int, score2: int) -> None:
    for _ in range(10):
        put_data('2' + player)
        put_data('6' + player)
    board, new_score1, new_score2 = get_board()
    assert player_str in board[0][9]
    assert score1 <= new_score1
    assert score2 <= new_score2


def move_left_and_down(player: str, player_str: str, score1: int, score2: int) -> None:
    for _ in range(10):
        put_data('4' + player)
        put_data('3' + player)
    board, new_score1, new_score2 = get_board()
    assert player_str in board[9][0]
    assert score1 <= new_score1
    assert score2 <= new_score2


def stroll_along(score1: int, score2: int, dir1: str, dir2: str, dir3: str) -> None:
    board, new_score1, new_score2 = get_board()
    assert score1 <= new_score1
    assert score2 <= new_score2
    score1 = new_score1
    score2 = new_score2

    direction = dir1
    for _ in range(10):
        for _ in range(10):
            result = put_data(direction + PLAYER1)
            print(result)
            if result != b'':
                new_score1, new_score2 = get_scores(result)
                assert score1 <= new_score1
                assert score2 == new_score2
            get_board()

        result = put_data(dir3 + PLAYER1)
        if result != b'':
            new_score1, new_score2 = get_scores(result)
            assert score1 <= new_score1
            assert score2 == new_score2
        get_board()

        direction = dir2 if direction == dir1 else dir1
    board, new_score1, new_score2 = get_board()
    for row in board:
        for col in row:
            assert '$' not in col
    assert score1 < new_score1
    assert score2 == new_score2


@pytest.mark.parametrize('execution_number', range(10))
def test_board(execution_number):
    board, score1, score2 = get_board()
    n = len(board)
    p1_loc = find_player(PLAYER1_STR, n, board)
    p2_loc = find_player(PLAYER2_STR, n, board)
    print("P1 Is in", p1_loc, "P2 is in", p2_loc)
    if p1_loc > p2_loc:
        move_left_and_down(PLAYER1, PLAYER1_STR, score1, score2)
        move_right_and_up(PLAYER2, PLAYER2_STR, score1, score2)
        for _ in range(10):
            put_data('4' + PLAYER2)
        stroll_along(score1, score2, '6', '4', '2')

    else:
        print(move_right_and_up(PLAYER1,PLAYER1_STR,score1,score2))
        print(move_left_and_down(PLAYER2,PLAYER2_STR,score1,score2))
        move_right_and_up(PLAYER1, PLAYER1_STR, score1, score2)
        move_left_and_down(PLAYER2, PLAYER2_STR, score1, score2)
        for _ in range(10):
            put_data('2' + PLAYER2)
        stroll_along(score1, score2, '4', '6', '3')


#
#  DO NOT CHANGE THE CODE ABOVE
#
