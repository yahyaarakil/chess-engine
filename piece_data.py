patterns = {
    "pawn_move": [
        [0, 1, 0],
        [0, 0, 0],
        [0, 0, 0]
    ],
    "pawn_attack": [
        [1, 0, 1],
        [0, 0, 0],
        [0, 0, 0]
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
        "move": (patterns["pawn_move"], ),
        "attack": (patterns["pawn_attack"], ),
        "reverse_move": True
    },
    "rook":{
        "value": 5,
        "move": (dimensions["vertical"], dimensions["horizontal"]),
        "attack": (dimensions["vertical"], dimensions["horizontal"]),
        "reverse_move": False
    }
}

class Piece:
    def __init__(self, piece_name, owner):
        self.piece_name = piece_name
        self.owner = owner