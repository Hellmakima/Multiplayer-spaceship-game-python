# Multiplayer-spaceship-game-python
[Screencast from 23-09-24 05:35:45 PM IST.webm](https://github.com/user-attachments/assets/44067bae-7ef1-40ff-be5d-f86845046731)

Multiplayer 2D spaceship game made with pygame and UDP sockets in python
Working:
12333 for initial contact with server to get its ip
12344 for server to client
12345 for client to server
client:
    sends:
current location
	new bullets created (location and dir)
    processes:
	renders what server sends (+current player)
	calculate other physics stuff
server:
    stores what client sends
    sends:
	list of player (locations)
	list of bullet (locations)
    processes:
	update bullets locations
	yet: identify bullet hits handle
	
To do:
 Make a module.py for main and let the server run it optionally in a thread.
 Implement max players.
 Let them add names.
