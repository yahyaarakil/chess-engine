#!/usr/bin/env python

import asyncio
import websockets
from helper import *
import sys
import time
sys.path.append("../core/")
from board_patterns import *
from board import *
from chess import *
from piece_data import *

players = {}
games = {}
sockets = {}
timers = {}

def new_player(message, socket):
    response = gen_id(20)
    while response in players:
        response = gen_id(20)
    players[response] = -1
    sockets[response] = socket
    return "id: " + response

async def new_game(message):
    if message[0] in games:
        if message[0] == games[message[0]][1]:
            other = games[message[0]][0]
        else:
            other = games[message[0]][1]
        sockets[other].send("other_dis")
    games[message[0]] = [Board("default"), message[0]]
    players[message[0]] = 0
    return "status: waiting"

async def join_game(message):
    games[message[0]] = games[message[2]]
    games[message[0]].append(message[0])
    await sockets[message[2]].send("status: in_game")
    players[message[0]] = 1
    return "status: in_game"

def generate_welcome(message):
    board = games[message[0]][0]
    welcome = "welcome "
    for row in board.tiles:
        for tile in row:
            if tile.piece_slot != None:
                piece = tile.piece_slot
                welcome += ">{},{},{},{},{},(".format(
                    piece.piece_name,
                    piece.owner,
                    piece.identifier,
                    tile.pos[0],
                    tile.pos[1]
                )
                for move in piece.move + piece.attack:
                    welcome += str(move.pos[0]) + "," + str(move.pos[1]) + ";"
                welcome += ")"
    welcome += ">" + str(players[message[0]])
    return welcome

async def interface(websocket, path):
    message = await websocket.recv()
    while True:
        print(f"< {message}")
        message = message.split(' ')
        if message[0] == "new_connection":
            response = new_player(message, websocket)
        elif message[1] == "new_game":
            response = await new_game(message)
        elif message[1] == "join_game":
            response = await join_game(message)
        elif message[1] == "welcome_me":
            response = generate_welcome(message)

        await websocket.send(response)
        print(f"> {response}")
        message = await websocket.recv()

start_server = websockets.serve(interface, "localhost", 5000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()