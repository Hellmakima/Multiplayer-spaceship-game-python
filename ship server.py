# Server
import socket
import threading
import time
import json

player_data = []
player_b_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
player_b_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

fps = 0.017  # 1/fps


def listen_to_client():
    player_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    player_socket.bind(('0.0.0.0', 12345))

    while True:
        data, player_address = player_socket.recvfrom(124)
        data = data.decode()
        print(f"Received message from client at {player_address}: '{data}'")
        if data == 'new':
            player_data.append((len(player_data), 0, 0))
        elif data.split(' ')[0] == 'bye':
            print('bye client')
            uid = data.split()[1]
            for player in player_data:
                if player[0] == uid:
                    player_data.remove(player)
                    break
        else:
            msg = eval(data)
            for i, player in enumerate(player_data):
                if player[0] == msg[0]:
                    player_data[i] = tuple(msg)
                    break


threading.Thread(target=listen_to_client, daemon=True).start()


def send_data():
    global player_data
    json_to_send = json.dumps(player_data)
    # print(f'sent{player_data}')
    player_b_socket.sendto(
        json_to_send.encode(), ('<broadcast>', 12344))


def run_player():
    import ship_player


# threading.Thread(None, target=run_player, daemon=True).start()
while True:
    time.sleep(fps)
    # print(player_data)
    send_data()
