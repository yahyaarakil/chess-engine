from tkinter import *
from board import *
from board_patterns import *
from piece_data import *

board = Board("default")
board.print_board()
print("{} bytes".format(len(pickle.dumps(board))))

root = Tk()

light_tile = PhotoImage(file='light.png')
dark_tile = PhotoImage(file='dark.png')

rendered = False
for row in board.tiles:
    for tile in row:
        label = Button(root)
        if tile.color == 1:
            label['image'] = dark_tile
        else:
            label['image'] = light_tile
        if tile.piece_slot != None:
            if tile.piece_slot.owner == "white":
                color = "Grey"
            else:
                color = "Black"
            lab = Label(label, text = tile.piece_slot.piece_name, fg = color)
            lab.pack()

        label.grid(row = tile.pos[1], column = tile.pos[0], ipadx = 0, ipady = 0, padx = 0, pady = 0)

root.mainloop()

# piece_pos = (1, 7)

# if board.tiles[piece_pos[1]][piece_pos[0]].piece_slot != None:
#     print("We have a {} on ({}, {})".format(board.tiles[piece_pos[1]][piece_pos[0]].piece_slot.piece_name,
#     piece_pos[0], piece_pos[1]))
#     print("It can move to: ")
#     for tile in board.tiles[piece_pos[1]][piece_pos[0]].piece_slot.move:
#         print("({}, {})".format(tile.pos[0], tile.pos[1]))
