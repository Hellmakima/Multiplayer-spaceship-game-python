# player / client
# network part
from pygame.math import Vector2
import pygame as p
import socket
import threading
import json


p.init()
width, height = 800, 800
width2, height2 = 500, 500
w = p.display.set_mode((width, height))
screen = p.Surface((width2, height2), p.SRCALPHA)
screen2 = p.Surface((width2, height2))
font = p.font.Font(None, 36)
clock = p.time.Clock()
fps = 60
mouse_down = False
click = Vector2(0, 0)
drag = Vector2(0, 0)
acc = Vector2(0, 0)
accmax = 10
vel = Vector2(0, 0)
velmax = accmax * 1.5
pos = Vector2(0, 0)
dir = Vector2(0, 0)

players = []  # (locations only (x,y))
bullets = []

uid = 0  # assigned by server

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('0.0.0.0', 12344))
server_address = ['localhost', 0]


def search_server():
    global uid, server_address
    # receive first packet to identify server
    data, server_address = server_socket.recvfrom(1024)
    server_socket.sendto(('new').encode(), (server_address[0], 12345))
    # server_socket.bind((server_address[0], 12344))
    player_list = eval(data.decode())
    if len(player_list) == 1:
        uid = 0
        return
    uid = int(player_list[-2][0] + 1)


threading.Thread(None, target=search_server, daemon=True).start()


color_list = []
for i in range(10):
    color_list.append(p.Color(((100 + i * 22) % 255),
                              ((200 + i * 93) % 255),
                              ((444 + i * 77) % 255)))


def update():
    global pos, vel, acc
    acc = click - drag
    try:
        acc.scale_to_length(min(acc.length(), accmax))
    except:
        pass
    vel += acc * .005
    try:
        vel.scale_to_length(min(vel.length(), velmax))
    except:
        pass
    pos -= vel
    if pos.x > height2/2 or pos.x < -height2/2:
        vel.x *= -1
    if pos.y > width2/2 or pos.y < -width2/2:
        vel.y *= -1
    text = font.render(
        # f'speed: {vel.length():.2f} acc: {acc.length():.2f} pos: {pos.x:.0f},{-pos.y:.0f}', False, 'white')
        f'velocity: {vel.x:.0f},{-vel.y:.0f} acc: {acc.x:.0f},{-acc.y:.0f} pos: {pos.x:.0f},{-pos.y:.0f}', False, 'white')
    w.blit(text, (0, 0))


def add_bullet():
    global pos, acc, server_address, dir
    msg = ("bullet", uid, pos.x, pos.y, dir.x, dir.y)
    json_to_dump = json.dumps(msg)
    server_socket.sendto(json_to_dump.encode(), (server_address[0], 12345))


def draw():
    global players, screen2, bullets
    # acc_angle = p.math.Vector2(1, 0).angle_to(acc)
    # p.draw.circle(trails, 'white', (pos.x + height2/2, pos.y + width2/2), 5)
    for player in players:
        # print(f'player in players: {player}')
        p.draw.circle(screen2, color_list[player[0] % len(color_list)],
                      (player[1] + height2/2, player[2] + width2/2), 5)
    p.draw.circle(screen2, color_list[uid],
                  (pos.x + height2/2, pos.y + width2/2), 5)
    for bullet in bullets:
        p.draw.circle(screen2, color_list[bullet[0] % len(color_list)],
                      (bullet[1] + height2/2, bullet[2] + width2/2), 5, 1)


def listen_to_server():
    '''
    collect a list/ dict containing all player ids and locations.
    yet to implement dict and collection of locations of bullets
    '''
    global players, bullets
    while True:
        data, server_address = server_socket.recvfrom(1024)
        received = eval(data.decode())
        bullets = received.pop()
        players = received
        # print(f'received from server:{players}')


threading.Thread(target=listen_to_server, daemon=True).start()


def send_location():
    '''
    send player's current location with id
    yet to implement bullets
    '''
    global server_address, pos
    msg = [uid, pos.x, pos.y]  # sending id to identify this ship
    # server_socket.sendto(str(msg).encode(), (server_address[0], 12345))
    json_to_send = json.dumps(msg)
    server_socket.sendto(json_to_send.encode(), (server_address[0], 12345))


while True:
    clock.tick(fps)
    w.fill('black')
    # p.draw.rect(s, 'red', p.Rect(0, 0, width2, height2), 1)
    for event in p.event.get():
        if event.type == p.QUIT:
            # print("bye")
            server_socket.sendto((('bye ' + str(uid))).encode(),
                                 (server_address[0], 12345))
            p.quit()
            exit()
        if event.type == p.MOUSEBUTTONDOWN:
            mouse_down = True
            click = Vector2(p.mouse.get_pos())
        if event.type == p.MOUSEBUTTONUP:
            mouse_down = False
            drag = click
        if event.type == p.KEYDOWN:
            # print('fuck')
            add_bullet()

    screen.fill((50, 50, 50, 255))
    w.blit(screen, (-pos.x - width2/2 + width/2, -pos.y - height2/2 + height/2))
    screen2.fill((50, 50, 50, 0))
    draw()
    w.blit(screen2, (-pos.x - width2/2 + width/2, -pos.y - height2/2 + height/2))

    if mouse_down:
        p.draw.circle(w, 'green', click, 40, 1)
        drag = Vector2(p.mouse.get_pos())
        dir = drag - click
        try:
            dir.normalize_ip()
        except:
            pass
        end = click + dir * 40
        p.draw.line(w, 'white', click, end)
    update()
    send_location()
    p.display.flip()
