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

def pawn_cond(piece):
    if piece.move_no == 0:
        return True
    return False

conds = {
    "pawn_cond": pawn_cond,
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
    ]
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
        "move": (("pattern", patterns["king"]), ),
        "attack": (("pattern", patterns["king"]), ),
        "reverse_move": False,
        "sprite": "king.png",
        "guarded": "king"
    }
}