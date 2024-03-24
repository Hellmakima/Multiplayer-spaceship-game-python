# Server
import socket
import threading
import time
import json
import pygame as p

width2, height2 = 500, 500
player_data = []
bullets = []
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
            player_data.insert(len(player_data), (len(player_data), 0, 0))
        elif data.split(' ')[0] == 'bye':
            uid = data.split()[1]
            print(f'uid {uid} left')
            for player in player_data:
                if player[0] == int(uid):
                    player_data.remove(player)
                    break
        else:
            msg = eval(data)
            if msg[0] == 'bullet':
                bullets.append(msg[1:])
                # print(msg)
                continue
            for i, player in enumerate(player_data):
                if player[0] == msg[0]:
                    player_data[i] = tuple(msg)
                    break


threading.Thread(target=listen_to_client, daemon=True).start()


def send_data():
    global player_data
    player_data.append(bullets)
    json_to_send = json.dumps(player_data)
    print(f'sent{player_data}')
    player_b_socket.sendto(
        json_to_send.encode(), ('<broadcast>', 12344))
    player_data.pop()


def run_player():
    import ship_player


def update_bullets():
    for bullet in bullets:
        dir = p.Vector2(bullet[3], bullet[4])
        try:
            dir.normalize_ip()
        except:
            bullets.remove(bullet)
            continue
        # end = click + dir * 40
        bullet[1] += 7 * dir.x
        bullet[2] += 7 * dir.y
        if bullet[1] > width2 or bullet[1] < -width2 or bullet[2] > height2 or bullet[2] < -height2:
            bullets.remove(bullet)
            continue


# threading.Thread(None, target=run_player, daemon=True).start()
while True:
    time.sleep(fps)
    update_bullets()
    # print(player_data)
    send_data()
