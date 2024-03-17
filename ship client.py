#network part
import socket
import threading

players = []#(locations only (x,y))
uid = 0 #changed later

server_socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#client listening at 12333 port for first msg
server_socket1.bind(('0.0.0.0', 12333))
#receive first packet to identify server
data, server_address = server_socket1.recvfrom(1024)
print(f"server first {server_address}: '{data.decode()}'")
uid = int(data.decode())
print(uid)
server_socket1.sendto('new'.encode(), (server_address[0], 12345))

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('0.0.0.0', 12344))


def listen_to_server():#gather info
    global server_address, players
    while True:
        data, server_address = server_socket.recvfrom(1024)
        players = eval(data.decode())
        #print(players)

server_thread = threading.Thread(target=listen_to_server, daemon = True)
server_thread.start()

#game part
import pygame as p
from pygame.math import Vector2

p.init()
width, height = 800, 800
width2, height2 = 500, 500

w = p.display.set_mode((width, height))
s = p.Surface((width2, height2), p.SRCALPHA)
trails = p.Surface((width2, height2), p.SRCALPHA)
font = p.font.Font(None, 36)
clock = p.time.Clock()

mouse_down = False
click = Vector2(0, 0)
drag = Vector2(0, 0)
vel = Vector2(0, 0)
acc = Vector2(0, 0)
velmax = 60
accmax = 20
pos = Vector2(0, 0)

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
        vel.x *= -.8
    if pos.y > width2/2 or pos.y < -width2/2:
        vel.y *= -.8
    
    
    # pos.x = max(min(height2/2,pos.x),-height2/2)
    # pos.y = max(min(width2/2,pos.y),-width2/2)
    text = font.render(f'speed: {vel.length():.2f} acc: {acc.length():.2f} pos: {pos.x:.0f},{pos.y:.0f}', False, 'white')
    w.blit(text, (0,0))

# help('pygame.draw.rect')


def draw_ship():
    global players
    #acc_angle = p.math.Vector2(1, 0).angle_to(acc)
    # p.draw.circle(trails, 'white', (pos.x + height2/2, pos.y + width2/2), 5)
    for ship in players:
        p.draw.circle(trails, 'white', (ship[0] + height2/2, ship[1] + width2/2), 5)

def send_data():
    global server_address, pos
    msg = (uid, pos.x, pos.y) #sending id to identify this ship
    server_socket.sendto(str(msg).encode(), (server_address[0], 12345))
    
while True:
    clock.tick(60)
    w.fill('black')
    s.fill((0,0,0,0))
    trails.fill((0,0,0,50))
    p.draw.rect(s,'red',p.Rect(0,0,width2,height2),4)
    for event in p.event.get():
        if event.type == p.QUIT:
            p.quit()
            exit()
        if event.type == p.MOUSEBUTTONDOWN:
            mouse_down = True
            click = Vector2(p.mouse.get_pos())
        if event.type == p.MOUSEBUTTONUP:
            mouse_down = False
            drag = click
    
    w.blit(s,(-pos.x - width2/2 + width/2, -pos.y - height2/2 + height/2))
    draw_ship()
    w.blit(trails,(-pos.x - width2/2 + width/2, -pos.y - height2/2 + height/2))
    
    if mouse_down:
        p.draw.circle(w, 'green', click, 60, 1)
        drag = Vector2(p.mouse.get_pos())
        dir = drag - click
        try:
            dir.normalize_ip()
        except:
            pass
        end = click + dir * 60
        p.draw.line(w, 'white', click, end)
    update()
    send_data()
    p.display.flip()