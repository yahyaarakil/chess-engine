import pickle
from board_patterns import *
from piece_data import *

class Tile:
    def __init__(self, color, pos):
        self.piece_slot = None
        self.color = color
        self.pos = pos

class Board:
    def __init__(self, board_pattern, tile_class = Tile):
        self.tiles = []
        self.board_pattern = board_pattern
        self.players = (board_dictionaries[board_pattern]["players"])[::]
        self. width = board_dictionaries[board_pattern]["dimensions"][0]
        self. height = board_dictionaries[board_pattern]["dimensions"][1]
        color = board_dictionaries[self.board_pattern]["tile_zero"]
        for y in range(8):
            self.tiles.append([])
            for x in range(8):
                self.tiles[y].append(tile_class(color, (x, y)))
                color *= -1
            color *= -1
        for piece_data in board_dictionaries[board_pattern]["pieces"]:
            print("Placing a {} {} at ({}, {})".format(piece_data[2], piece_data[1], piece_data[0][0], piece_data[0][1]))
            self.place_piece(piece_data[0], Piece(piece_data[1], piece_data[2], piece_dictionaries[piece_data[1]]["sprite"]))
        y = self.height - 1
        for row in self.tiles:
            x = 0
            for tile in row:
                if tile.piece_slot != None:
                    self.calc_move(tile.piece_slot, (x, y))
                x += 1
            y -= 1
    
    def place_piece(self, pos, piece):
        self.tiles[pos[1]][pos[0]].piece_slot = piece

    def print_board(self):
        for row in self.tiles:
            for cell in row:
                if cell.color == 1:
                    print("# ", end = "")
                else:
                    print("O ", end = "")
            print("")

    def calc_move(self, piece, pos):
        piece.move = []
        move_pattern = piece_dictionaries[piece.piece_name]["move"]
        attack_pattern =  piece_dictionaries[piece.piece_name]["attack"]
        for pattern in move_pattern:
            if pattern[0] == "pattern":
                pat = pattern[1][:]
                if piece_dictionaries[piece.piece_name]["reverse_move"]\
                    and piece.owner == "black":
                    pat.reverse()
                self.find_pattern(piece, pos, "move", pat)
            elif pattern[0] == "dimension":
                self.find_dimension(piece, pos, "move", pattern[1])
        for pattern in attack_pattern:
            if pattern[0] == "pattern":
                pat = pattern[1][:]
                if piece_dictionaries[piece.piece_name]["reverse_move"]\
                    and piece.owner == "black":
                    pat.reverse()
                self.find_pattern(piece, pos, "attack", pat)
            elif pattern[0] == "dimension":
                self.find_dimension(piece, pos, "attack", pattern[1])

    def find_dimension(self, piece, pos, pattern_name, pattern):
        pass

        
    def find_pattern(self, piece, pos, pattern_name, pattern):
        x = pos[0] - len(pattern[0])//2
        y = pos[1] + len(pattern)//2
        yy = y
        for row in pattern:
            xx = x
            if yy < 0 or yy > self.height - 1:
                yy -= 1
                continue
            for cell in row:
                if cell == 0:
                    xx += 1
                    continue
                if xx < 0 or xx > self.width - 1:
                    xx += 1
                    continue
                print("checking")
                if self.tiles[yy][xx].piece_slot == None:
                    if pattern_name == "move":
                        if not self.tiles[yy][xx] in piece.move\
                            and not self.tiles[yy][xx] in piece.attack:
                            yyy = yy + 3
                            if yyy >= self.height - 1:
                                yyy -= 6
                            piece.move.append(self.tiles[yyy][xx])
                            print("appending to {}".format(piece.piece_name))
                else:
                    if self.tiles[yy][xx].piece_slot.owner != piece.owner\
                        and pattern_name == "attack":
                        if not self.tiles[yy][xx] in piece.move\
                            and not self.tiles[yy][xx] in piece.attack:
                            yyy = yy + 3
                            if yyy > self.height - 1:
                                yyy -= 6
                            piece.attack.append(self.tiles[yy][xx])
                            print("appending to {}".format(piece.piece_name))
                xx += 1
            yy -= 1

    def kill(self, piece):
        del piece

    def move(self, from_tile, to_tile):
        print("MOVING!")
        if from_tile.piece_slot == None:
            print("NOPE!")
            return
        if to_tile.piece_slot != None:
            self.kill(to_tile.piece_slot)
        to_tile.piece_slot = from_tile.piece_slot
        from_tile.piece_slot = None
        self.calc_move(to_tile.piece_slot, to_tile.pos)

