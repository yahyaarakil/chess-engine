class Piece:
    identifiers = 0
    def __init__(self, piece_name, owner):
        self.last_moved = -1
        self.piece_name = piece_name
        self.owner = owner
        self.move = []
        self.attack = []
        self.move_no = 0
        self.is_attacked = False
        self.identifier = Piece.identifiers
        Piece.identifiers += 1

def pawn_init(piece, pos, board):
    piece.double_move = False

def pawn_cond(piece, pos, board):
    if piece.move_no == 0:
        return True
    return False

def double_move_fun(piece, pos, board):
    piece.double_move = True

def double_move_prune(piece, pos, board):
    return False

# King side
def move_king_rook(piece, pos, board):
    board.move_unchecked(board.tiles[pos[1]][board.width-1], board.tiles[pos[1]][pos[0]+1])

def king_side_cond(piece, pos, board):
    if piece.move_no == 0:
        if piece.is_attacked:
            return False
        if pos[0]+3 > board.width - 1:
            return False
        rook = board.tiles[pos[1]][board.width-1].piece_slot
        if rook != None:
            if rook.piece_name == "rook" and rook.move_no == 0 and rook.owner == piece.owner:
                for tile_index in range(board.width-1-pos[0]-1):
                    selection = pos[0] + 1 + tile_index
                    if board.tiles[pos[1]][selection].piece_slot != None:
                        return False
                return True
    return False

def king_side_prune(piece, pos, board):
    for tile_index in range(board.width-1-pos[0]-1):
        selection = pos[0] + 1 + tile_index
        for row in board.tiles:
            for tile in row:
                if tile.piece_slot != None:
                    if tile.piece_slot.owner != piece.owner:
                        if board.tiles[pos[1]][selection] in tile.piece_slot.move:
                            return True
    return False

# Queen side
def move_queen_rook(piece, pos, board):
    board.move_unchecked(board.tiles[pos[1]][0], board.tiles[pos[1]][pos[0]-1])

def queen_side_cond(piece, pos, board):
    if piece.move_no == 0:
        if piece.is_attacked:
            return False
        if pos[0]-4 < 0:
            return False
        rook = board.tiles[pos[1]][0].piece_slot
        if rook != None:
            if rook.piece_name == "rook" and rook.move_no == 0 and rook.owner == piece.owner:
                for tile_index in range(pos[0]-1):
                    selection = 1 + tile_index
                    if board.tiles[pos[1]][selection].piece_slot != None:
                        return False
                return True
    return False

def queen_side_prune(piece, pos, board):
    for tile_index in range(pos[0]-1):
        selection = 1 + tile_index
        for row in board.tiles:
            for tile in row:
                if tile.piece_slot != None:
                    if tile.piece_slot.owner != piece.owner:
                        if board.tiles[pos[1]][selection] in tile.piece_slot.move:
                            return True
    return False

# En passant

def en_passant_kill_right(piece, pos, board):
    board.kill((pos[0] + 1, pos[1]))

def en_passant_cond_right(piece, pos, board):
    x = pos[0] + 1
    if x > board.width - 1:
        return False
    piece_right = board.tiles[pos[1]][x].piece_slot
    if piece_right == None:
        return False
    if piece_right.owner == piece.owner:
        return False
    if piece_right.piece_name != "pawn":
        return False
    if not piece_right.double_move:
        return False
    if piece_right.last_moved == board.turn_no - 1:
        return True
    return False

def en_passant_kill_left(piece, pos, board):
    board.kill((pos[0] - 1, pos[1]))

def en_passant_cond_left(piece, pos, board):
    x = pos[0] - 1
    if x < 0:
        return False
    piece_left = board.tiles[pos[1]][x].piece_slot
    if piece_left == None:
        return False
    if piece_left.owner == piece.owner:
        return False
    if piece_left.piece_name != "pawn":
        return False
    if not piece_left.double_move:
        return False
    if piece_left.last_moved == board.turn_no - 1:
        return True
    return False


conds = {
    "pawn_cond": pawn_cond,
    "double_move_fun": double_move_fun,
    "double_move_prune": double_move_prune,

    "king_side_cond": king_side_cond,
    "move_king_rook": move_king_rook,
    "king_side_prune": king_side_prune,

    "queen_side_cond": queen_side_cond,
    "move_queen_rook": move_queen_rook,
    "queen_side_prune": queen_side_prune,

    "en_passant_kill_right": en_passant_kill_right,
    "en_passant_cond_right": en_passant_cond_right,
    "en_passant_kill_left": en_passant_kill_left,
    "en_passant_cond_left": en_passant_cond_left,
}
        
patterns = {
    "pawn_move": [
        [0, 1, 0],
        [0, 0, 0],
        [0, 0, 0]
    ],
    "pawn_move1": [
        [0, 0, 5, 0, 0],
        [0, 0, 5, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ],
    "pawn_attack1": [
        [1, 0, 0],
        [0, 0, 0],
        [0, 0, 0]
    ],
    "pawn_attack2": [
        [0, 0, 1],
        [0, 0, 0],
        [0, 0, 0]
    ],
    "knight": [
        [0, 1, 0, 1, 0],
        [1, 0, 0, 0, 1],
        [0, 0, 0, 0, 0],
        [1, 0, 0, 0, 1],
        [0, 1, 0, 1, 0]
    ],
    "king": [
        [1, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ],
    "king_side": [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ],
    "queen_side": [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ],
}

dimensions = {
    "vertical": [
        [0, 1, 0],
        [0, 0, 0],
        [0, 1, 0],
    ],
    "horizontal": [
        [0, 0, 0],
        [1, 0, 1],
        [0, 0, 0],
    ],
    "diag1": [
        [1, 0, 0],
        [0, 0, 0],
        [0, 0, 1],
    ],
    "diag2": [
        [0, 0, 1],
        [0, 0, 0],
        [1, 0, 0],
    ]
}

piece_dictionaries = {
    "pawn":{
        "value": 1,
        "move": (("pattern", patterns["pawn_move"]),
        ("pattern", patterns["pawn_move1"], "pawn_cond", "double_move_fun", "double_move_prune"),
        ("pattern", patterns["pawn_attack2"], "en_passant_cond_right", "en_passant_kill_right", "double_move_prune"),
        ("pattern", patterns["pawn_attack1"], "en_passant_cond_left", "en_passant_kill_left", "double_move_prune"),),
        "attack": (("pattern", patterns["pawn_attack1"]),
        ("pattern", patterns["pawn_attack2"]),),
        "reverse_move": True,
        "init": pawn_init,
        "promotes": ("rook", "bishop", "knight", "queen")
    },
    "rook":{
        "value": 5,
        "move": (("dimension", dimensions["vertical"]), ("dimension", dimensions["horizontal"])),
        "attack": (("dimension", dimensions["vertical"]), ("dimension", dimensions["horizontal"])),
        "reverse_move": False,
    },
    "knight":{
        "value": 3,
        "move": (("pattern", patterns["knight"]), ),
        "attack": (("pattern", patterns["knight"]), ),
        "reverse_move": False,
    },
    "bishop":{
        "value": 3,
        "move": (("dimension", dimensions["diag1"]), ("dimension", dimensions["diag2"])),
        "attack": (("dimension", dimensions["diag1"]), ("dimension", dimensions["diag2"])),
        "reverse_move": False,
    },
    "queen":{
        "value": 9,
        "move": (("dimension", dimensions["diag1"]), ("dimension", dimensions["diag2"]), ("dimension", dimensions["vertical"]), ("dimension", dimensions["horizontal"])),
        "attack": (("dimension", dimensions["diag1"]), ("dimension", dimensions["diag2"]), ("dimension", dimensions["vertical"]), ("dimension", dimensions["horizontal"])),
        "reverse_move": False,
    },
    "king":{
        "value": 0,
        "move": (("pattern", patterns["king"]),
        ("pattern", patterns["king_side"], "king_side_cond", "move_king_rook", "king_side_prune"),
        ("pattern", patterns["queen_side"], "queen_side_cond", "move_queen_rook", "queen_side_prune"),),
        "attack": (("pattern", patterns["king"]), ),
        "reverse_move": False,
        "guarded": "king"
    }
}