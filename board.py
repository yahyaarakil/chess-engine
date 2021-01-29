import pickle
from board_patterns import *
from piece_data import *

class Tile:
    def __init__(self, color):
        self.piece_slot = None
        self.color = color

class Board:
    def __init__(self, board_pattern):
        self.tiles = []
        self.board_pattern = board_pattern
        self.players = (board_dictionaries[board_pattern]["players"])[::]
        color = board_dictionaries[self.board_pattern]["tile_zero"]
        for y in range(8):
            self.tiles.append([])
            for x in range(8):
                self.tiles[y].append(Tile(color))
                color *= -1
            color *= -1
        for piece_data in board_dictionaries[board_pattern]["pieces"]:
            print("Placing a {} at ({}, {})".format(piece_data[1], piece_data[0][0], piece_data[0][1]))
            self.place_piece(piece_data[0], Piece(piece_data[1], piece_data[2]))
    
    def place_piece(self, pos, piece):
        self.tiles[pos[0]][pos[1]].piece_slot = piece

    def print_board(self):
        for row in self.tiles:
            for cell in row:
                if cell.color == 1:
                    print("# ", end = "")
                else:
                    print("O ", end = "")
            print("")
    
board = Board("default")
board.print_board()
print("{} bytes".format(len(pickle.dumps(board))))