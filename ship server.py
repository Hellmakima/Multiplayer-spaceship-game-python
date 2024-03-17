# Server (Broadcasting)
import socket
import threading
import time
import json

count = 0
player = []
client_list = []
client_broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

server_address = ('<your_server_ip>', 12345)

def listen_to_client():
    global count
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.bind(('0.0.0.0', 12345))

    while True:
        data, client_address = client_socket.recvfrom(1024)
        data = data.decode()
        print(f"Received message from client at {client_address}: '{data}'")
        if data == 'new':
            client_list.append(client_address)
            player.append((count, 0, 0))
            count += 1
        else:
            msg = eval(data)
            player[msg[0]] = (msg[1], msg[2])
def send_data():
    global player, client_list
    json_to_send = json.dumps(player)
    for client in client_list:
        client_broadcast_socket.sendto(json_to_send.encode(), (client[0],12344))

def broadcast():
    global count
    while True:
        time.sleep(1)
        client_broadcast_socket.sendto(str(count).encode(), ('<broadcast>', 12333))

client_thread = threading.Thread(target = listen_to_client, daemon = True)
client_thread.start()
broadcast_thread = threading.Thread(target = broadcast, daemon = True)
broadcast_thread.start()

while True:
    # time.sleep(.01)
    print(player)
    send_data()