class Piece:
    identifiers = 0
    def __init__(self, piece_name, owner, sprite_name):
        self.piece_name = piece_name
        self.owner = owner
        self.move = []
        self.attack = []
        self.sprite_name = sprite_name
        self.move_no = 0
        self.is_attacked = False
        self.identifier = Piece.identifiers
        Piece.identifiers += 1

def pawn_cond(piece, pos, board):
    if piece.move_no == 0:
        return True
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

conds = {
    "pawn_cond": pawn_cond,

    "king_side_cond": king_side_cond,
    "move_king_rook": move_king_rook,
    "king_side_prune": king_side_prune,

    "queen_side_cond": queen_side_cond,
    "move_queen_rook": move_queen_rook,
    "queen_side_prune": queen_side_prune,
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
    "pawn_attack": [
        [1, 0, 1],
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
        "move": (("pattern", patterns["pawn_move"]), ("pattern", patterns["pawn_move1"], "pawn_cond"),),
        "attack": (("pattern", patterns["pawn_attack"]), ),
        "reverse_move": True,
        "sprite": "pawn.png"
    },
    "rook":{
        "value": 5,
        "move": (("dimension", dimensions["vertical"]), ("dimension", dimensions["horizontal"])),
        "attack": (("dimension", dimensions["vertical"]), ("dimension", dimensions["horizontal"])),
        "reverse_move": False,
        "sprite": "rook.png"
    },
    "knight":{
        "value": 3,
        "move": (("pattern", patterns["knight"]), ),
        "attack": (("pattern", patterns["knight"]), ),
        "reverse_move": False,
        "sprite": "knight.png"
    },
    "bishop":{
        "value": 3,
        "move": (("dimension", dimensions["diag1"]), ("dimension", dimensions["diag2"])),
        "attack": (("dimension", dimensions["diag1"]), ("dimension", dimensions["diag2"])),
        "reverse_move": False,
        "sprite": "bishop.png"
    },
    "queen":{
        "value": 9,
        "move": (("dimension", dimensions["diag1"]), ("dimension", dimensions["diag2"]), ("dimension", dimensions["vertical"]), ("dimension", dimensions["horizontal"])),
        "attack": (("dimension", dimensions["diag1"]), ("dimension", dimensions["diag2"]), ("dimension", dimensions["vertical"]), ("dimension", dimensions["horizontal"])),
        "reverse_move": False,
        "sprite": "queen.png"
    },
    "king":{
        "value": 0,
        "move": (("pattern", patterns["king"]),
        ("pattern", patterns["king_side"], "king_side_cond", "move_king_rook", "king_side_prune"),
        ("pattern", patterns["queen_side"], "queen_side_cond", "move_queen_rook", "queen_side_prune"),),
        "attack": (("pattern", patterns["king"]), ),
        "reverse_move": False,
        "sprite": "king.png",
        "guarded": "king"
    }
}