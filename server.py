
import socket

def play_game(is_server):
    if is_server:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', 60003))
        server_socket.listen(1)

        print('\nWaiting for a connection...\n')

        (client_socket, addr) = server_socket.accept()
        print('Connection from {}'.format(addr))

    else:
        host = input("Enter the server's name or IP: ")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, 60003))
        print('Connected to the server')

    player_score = 0
    opponent_score = 0

    while player_score < 10 and opponent_score < 10:
        print(f'({player_score},{opponent_score}) Your move: ', end='')
        player_move = input().upper()

        while player_move not in {"R", "P", "S"}:
            print('Invalid move. Enter R, P, or S: ', end='')
            player_move = input().upper()

        client_socket.sendall(bytearray(player_move, 'ascii'))
        print('Sent:', player_move)

        opponent_move = client_socket.recv(1024).decode('ascii')
        print('Opponent\'s move:', opponent_move)

       
        if player_move == opponent_move:
            print('Round tied!')
        elif (
            (player_move == 'R' and opponent_move == 'S') or
            (player_move == 'S' and opponent_move == 'P') or
            (player_move == 'P' and opponent_move == 'R')
        ):
            print('You win this round!')
            player_score += 1
        else:
            print('You lose this round.')
            opponent_score += 1

    if player_score > opponent_score:
        print(f'You won {player_score} against {opponent_score}')
    elif player_score < opponent_score:
        print(f'You lost with {player_score} against {opponent_score}')
    else:
        print(f'The game ended in a tie with a score of {player_score} against {opponent_score}')

    client_socket.close()

if __name__ == "__main__":
    ans = input("Do you want to be server (S) or client (C): ").upper()
    play_game(ans == "S")
