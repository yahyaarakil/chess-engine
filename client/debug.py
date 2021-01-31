import sys
sys.path.append("../core/")
from board_patterns import *
from board import *
from chess import *
from piece_data import *

def piece_to_token(piece):
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

def render_board(board):
    print("")
    for row in board.tiles:
        print("\n"+"*"*(5*board.width+1)+"\n*", end = "")
        for tile in row:
            if tile.selected:
                print("(", end = "")
            else:
                print(" ", end = "")
            print(piece_to_token(tile.piece_slot), end = "")
            if tile.selected:
                print(")", end = "")
            else:
                print(" ", end = "")
            print("*", end = "")
    print("\n"+"*"*(5*board.width+1) + "\n\n")

if __name__ == "__main__":
    my_board = Board("default")
    render_board(my_board)