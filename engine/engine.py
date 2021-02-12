import sys
sys.path.append("../core/")
from board_patterns import *
from board import *
from chess import *
from piece_data import *

class Engine:
    def copy_board(self, board):
        board = Board(board.board_pattern, board.tile_class, False)
        board.copy_board(ref_board = board)
        board.refresh_moves()
        return board

    def __init__(self, board):
        self.board = self.copy_board(board)

    def hypo_move(self, from_tile, to_tile, board = None):
        if board == None:
            board = self.board
        board.copy_board(board)
        board.move(from_tile, to_tile)
        return board

    def find_best_moves(self, player, depth, board = None):
        if board == None:
            board = self.board
        pieces = board.players[player][0] + board.players[player][1]

        move_outcomes = []
        move_values = []

        for row in board.tiles:
            for tile in row:
                piece = tile.piece_slot
                if piece != None:
                    if piece.owner == player:
                        for move in piece.move + piece.attack:
                            hypo_board = self.hypo_move(tile, move)
                            move_outcomes.append(hypo_board)
                            move_values.append(hypo_board.evaluate_for(player))

        losing = True
        for value in move_values:
            if value == float("inf"):
                index = move_values.index(value)
                return ([move_outcomes[index]], [move_values[index]])
            elif value != -float("inf"):
                losing = False

        if losing:
            return -1

        trees = []

        if depth > 0:
            for outcome in move_outcomes:
                trees.append(self.find_best_moves(board.other_player(player), depth-1, outcome))
        else:
            maximum = max(move_values)
            to_remove = []
            for index in range(len(move_values)):
                if move_values[index] < maximum:
                    to_remove.append(index)
            for index in to_remove:
                move_values.remove(move_values[index])
                move_outcomes.remove(move_outcomes[index])
            return (move_outcomes, move_values)
