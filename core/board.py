import pickle
from board_patterns import *
from piece_data import *

class Tile:
    def __init__(self, color, pos):
        self.piece_slot = None
        self.color = color
        self.pos = pos

class Board:
    def __init__(self, board_pattern, tile_class = Tile, load = True):
        self.tiles = []
        self.tile_class = tile_class
        self.board_pattern = board_pattern
        self.players = {}
        for player in (board_dictionaries[board_pattern]["players"]):
            self.players[player] = [[], []]
        self. width = board_dictionaries[board_pattern]["dimensions"][0]
        self. height = board_dictionaries[board_pattern]["dimensions"][1]
        color = board_dictionaries[self.board_pattern]["tile_zero"]
        for y in range(8):
            self.tiles.append([])
            for x in range(8):
                self.tiles[y].append(tile_class(color, (x, y)))
                color *= -1
            color *= -1
        if load:
            self.load_pattern(board_pattern)

    def load_pattern(self, board_pattern):
        for piece_data in board_dictionaries[board_pattern]["pieces"]:
            self.place_piece(piece_data[0], Piece(piece_data[1], piece_data[2], piece_dictionaries[piece_data[1]]["sprite"]))
        self.refresh_moves()

    def copy_board(self, ref_board):
        for row in ref_board.tiles:
            for tile in row:
                if tile.piece_slot != None:
                    self.place_piece(tile.pos, Piece(tile.piece_slot.piece_name, tile.piece_slot.owner, tile.piece_slot.sprite_name))

    def check_loss(self, player):
        for piece in self.players[player][0] + self.players[player][1]:
            if len(piece.move) != 0 or len(piece.attack) != 0:
                return "Not loss"
        for piece in self.players[player][0]:
            if piece.is_attacked:
                return "loss"
        return "stalemate"

    def prune_moves(self):
        for row in self.tiles:
            for tile in row:
                if tile.piece_slot != None:
                    for move in tile.piece_slot.move + tile.piece_slot.attack:
                        temp_board = Board(self.board_pattern, self.tile_class, False)
                        temp_board.copy_board(ref_board = self)
                        temp_board.move_unchecked(temp_board.tiles[tile.pos[1]][tile.pos[0]], temp_board.tiles[move.pos[1]][move.pos[0]])
                        temp_board.refresh_moves(False)
                        for piece in temp_board.players[tile.piece_slot.owner][0]:
                            if piece.is_attacked:
                                if move in tile.piece_slot.move:
                                    tile.piece_slot.move.remove(move)
                                else:
                                    tile.piece_slot.attack.remove(move)

    
    def refresh_moves(self, check = True):
        for row in self.tiles:
            for tile in row:
                if tile.piece_slot != None:
                    tile.piece_slot.is_attacked = False
        y = 0
        for row in self.tiles:
            x = 0
            for tile in row:
                if tile.piece_slot != None:
                    self.calc_move(tile.piece_slot, (x, y))
                x += 1
            y += 1
        if check:
            self.prune_moves()
    
    def place_piece(self, pos, piece):
        self.tiles[pos[1]][pos[0]].piece_slot = piece
        if "guarded" in piece_dictionaries[piece.piece_name]:
            self.players[piece.owner][0].append(piece)
        else:
            self.players[piece.owner][1].append(piece)

    def calc_move(self, piece, pos):
        piece.move = []
        piece.attack = []
        move_pattern = piece_dictionaries[piece.piece_name]["move"]
        attack_pattern =  piece_dictionaries[piece.piece_name]["attack"]
        for pattern in move_pattern:
            if len(pattern) == 3:
                if not conds[pattern[2]](piece):
                    continue
            if pattern[0] == "pattern":
                pat = pattern[1][:]
                if piece_dictionaries[piece.piece_name]["reverse_move"]\
                    and piece.owner == "black":
                    pat.reverse()
                self.find_pattern(piece, pos, "move", pat)
            elif pattern[0] == "dimension":
                self.find_dimension(piece, pos, "move", pattern[1])
        for pattern in attack_pattern:
            if len(pattern) == 3:
                if not conds[pattern[2]](piece):
                    continue
            if pattern[0] == "pattern":
                pat = pattern[1][:]
                if piece_dictionaries[piece.piece_name]["reverse_move"]\
                    and piece.owner == "black":
                    pat.reverse()
                self.find_pattern(piece, pos, "attack", pat)
            elif pattern[0] == "dimension":
                self.find_dimension(piece, pos, "attack", pattern[1])
        for tile in piece.attack:
            tile.piece_slot.is_attacked = True

    def find_dimension(self, piece, pos, pattern_name, pattern):
        pos_y = pos[1] - len(pattern)//2
        for row in range(len(pattern)):
            pos_x = pos[0] - len(pattern[row])//2
            for column in range(len(pattern[row])):
                if pattern[row][column] == 1:
                    if pos_x < self.width and pos_x > -1\
                        and pos_y < self.height and pos_y > -1:
                        #latch
                        vector = [pos_x - pos[0], pos_y - pos[1]]
                        selection_x = pos_x
                        selection_y = pos_y
                        while(True):
                            #do
                            if selection_x > self.width - 1 or selection_x < 0\
                                or selection_y > self.height - 1 or selection_y < 0:
                                break
                            if self.tiles[selection_y][selection_x].piece_slot == None:
                                piece.move.append(self.tiles[selection_y][selection_x])
                            else:
                                if self.tiles[selection_y][selection_x].piece_slot.owner == piece.owner:
                                    break
                                else:
                                    piece.attack.append(self.tiles[selection_y][selection_x])
                                    break
                            selection_x += vector[0]
                            selection_y += vector[1]
                pos_x += 1
            pos_y += 1

        
    def find_pattern(self, piece, pos, pattern_name, pattern):
        possilbe_count = 0
        possible = []
        pos_y = pos[1] - len(pattern)//2
        for row in range(len(pattern)):
            pos_x = pos[0] - len(pattern[row])//2
            for column in range(len(pattern[row])):
                if pattern[row][column] == 1 or pattern[row][column] == 5:
                    if pos_x < self.width and pos_x > -1\
                        and pos_y < self.height and pos_y > -1:
                        possilbe_count += 1
                        if self.tiles[pos_y][pos_x].piece_slot == None and pattern_name == "move":
                            if pattern[row][column] == 1:
                                piece.move.append(self.tiles[pos_y][pos_x])
                            else:
                                possible.append((self.tiles[pos_y][pos_x], "move"))
                        elif self.tiles[pos_y][pos_x].piece_slot != None and pattern_name == "attack":
                            if self.tiles[pos_y][pos_x].piece_slot.owner != piece.owner:
                                if pattern[row][column] == 1:
                                    piece.attack.append(self.tiles[pos_y][pos_x])
                                else:
                                    possible.append((self.tiles[pos_y][pos_x], "attack"))
                pos_x += 1
            pos_y += 1
        if possilbe_count == len(possible):
            for tile in possible:
                if tile[1] == "move":
                    piece.move.append(tile[0])
                elif tile[1] == "attack":
                    piece.attack.append(tile[0])

    def kill(self, piece):
        if piece in self.players[piece.owner][1]:
            self.players[piece.owner][1].remove(piece)
        del piece

    def move(self, from_tile, to_tile):
        if from_tile.piece_slot == None:
            return
        if to_tile in from_tile.piece_slot.move + from_tile.piece_slot.attack:
            self.move_unchecked(from_tile, to_tile)
            self.refresh_moves()
            return True
        return False

    def move_unchecked(self, from_tile, to_tile):
        if to_tile.piece_slot != None:
            self.kill(to_tile.piece_slot)
        to_tile.piece_slot = from_tile.piece_slot
        from_tile.piece_slot = None
        to_tile.piece_slot.move_no += 1
        return True


