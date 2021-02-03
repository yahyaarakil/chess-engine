import sys
sys.path.append("../core/")
from board_patterns import *
from board import *
from chess import *
from piece_data import *

class TileDebug(Tile):
    def __init__(self, color, pos):
        Tile.__init__(self, color, pos)
        self.selected = False
        self.highlighted = False

class BoardDebug(Board):
    def __init__(self, board_pattern):
        Board.__init__(self, board_pattern, TileDebug)
    def dehighlight(self):
        for row in self.tiles:
            for tile in row:
                tile.selected = False
                tile.highlighted = False

class Debug:
    def __init__(self):
        self.selected = None
    def piece_to_token(self, piece):
        if piece is None:
            return "  "
        else:
            token = ""
            if piece.owner == "white":
                token += "w"
            else:
                token += "b"
            if piece.piece_name == "king":
                token += "K"
            else:
                token += piece.piece_name[0]
            return token

    def render_tile_mode_end(self, tile):
        if tile.selected:
            print(")", end = "")
        elif tile.highlighted:
            print("|", end = "")
        else:
            print(" ", end = "")

    def render_tile_mode_start(self, tile):
        if tile.selected:
            print("(", end = "")
        elif tile.highlighted:
            print("|", end = "")
        else:
            print(" ", end = "")

    def render_board(self, board):
        string = ""
        string+='\n'
        row_no = 0
        for row in board.tiles:
            string+=("\n "+"*"*(5*board.width+1)+"\n"+str(row_no)+"*")
            row_no += 1
            for tile in row:
                self.render_tile_mode_start(tile)
                string+=(self.piece_to_token(tile.piece_slot))
                self.render_tile_mode_end(tile)
                string+=("*")
        string+=("\n "+"*"*(5*board.width+1)+"\n")
        for i in range(board.width):
            string+=("    {}".format(i))
        string+=("\n\n\n")

    def deselect(self, my_board):
        if self.selected == None:
            return
        tile = self.selected
        if tile.piece_slot != None:
            for tile_h in tile.piece_slot.move + tile.piece_slot.attack:
                tile_h.highlighted = False
        tile.selected = False
        tile.highlighted = False
        self.selected = None

    def select_tile(self, tile, my_board):
        self.deselect(my_board)
        if tile.piece_slot != None:
            self.selected = tile
            tile.selected = True
            tile.highlighted = False
            for tile_h in tile.piece_slot.move + tile.piece_slot.attack:
                tile_h.highlighted = True

    def interface(self, my_board, x, y, player):
        clicked_at_tile = my_board.tiles[y][x]
        if clicked_at_tile.piece_slot != None:
            if self.selected != None:
                if clicked_at_tile.piece_slot.owner == player:
                    self.select_tile(clicked_at_tile, my_board)
                elif clicked_at_tile in self.selected.piece_slot.attack:
                    my_board.move(self.selected, clicked_at_tile)
                    return True
            elif clicked_at_tile.piece_slot.owner == player:
                self.select_tile(clicked_at_tile, my_board)
        else:
            if clicked_at_tile in self.selected.piece_slot.move:
                my_board.move(self.selected, clicked_at_tile)
                return True
            else:
                my_board.select_tile(clicked_at_tile, my_board)
            debug.select_tile(my_board.tiles[y][x], my_board)
        return False

if __name__ == "__main__":
    my_board = BoardDebug("default")
    debug = Debug()
    player = 0
    players = ["white", "black"]
    while(True):
        try:
            print(debug.render_board(my_board))
            print("{}'s turn".format(players[player]))
            los_con = my_board.check_loss(players[player])
            if los_con == "loss":
                print(players[player], "LOST!")
                break
            elif los_con == "stalemate":
                print("STALEMATE!")
                break
            x = int(input("x: "))
            y = int(input("y: "))
            if debug.interface(my_board, x, y, players[player]):
                if debug.selected != None:
                    debug.deselect(my_board)
                player += 1
                if player == 2:
                    player = 0
                my_board.dehighlight()
        except Exception as e:
            print(e)