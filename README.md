# Multiplayer-spaceship-game-python
Multiplayer 2D spaceship game made with pygame and UDP sockets in python
Working:
12333 for initial contact with server to get its ip
12344 for server to client
12345 for client to server
client:
    sends:
	new bullets created (location and dir)
	current location
    processes:
	renders what server sends (+current player)
	calculate other physics stuff
server:
    stores what client sends
    sends:
	list of bullet (locations)
	list of player (locations)
    processes:
	update bullets locations
	identify bullet hits handle
	
Yet:
 Make a module.py for main and let the server run it optionally in a thread.
 Make changes to module to add bullets separately.
 Bye message to release id
 Implement unique colours to players.
 Maybe implement max players.
 Maybe let them add names.
 
