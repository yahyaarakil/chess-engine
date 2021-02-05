board_dictionaries = {
    "default":{
        "players": ("white", "black"),
        "dimensions": (8, 8),
        "tile_zero": -1,
        "pieces":[
            #black
            ((0, 1), "pawn", "black"),
            ((1, 1), "pawn", "black"),
            ((2, 1), "pawn", "black"),
            ((3, 1), "pawn", "black"),
            ((4, 1), "pawn", "black"),
            ((5, 1), "pawn", "black"),
            ((6, 1), "pawn", "black"),
            ((7, 1), "pawn", "black"),

            ((0, 0), "rook", "black"),
            ((7, 0), "rook", "black"),

            ((1, 0), "knight", "black"),
            ((6, 0), "knight", "black"),

            ((2, 0), "bishop", "black"),
            ((5, 0), "bishop", "black"),

            ((3, 0), "queen", "black"),
            ((4, 0), "king", "black"),

            #white
            ((0, 6), "pawn", "white"),
            ((1, 6), "pawn", "white"),
            ((2, 6), "pawn", "white"),
            ((3, 6), "pawn", "white"),
            ((4, 6), "pawn", "white"),
            ((5, 6), "pawn", "white"),
            ((6, 6), "pawn", "white"),
            ((7, 6), "pawn", "white"),

            ((0, 7), "rook", "white"),
            ((7, 7), "rook", "white"),

            ((1, 7), "knight", "white"),
            ((6, 7), "knight", "white"),

            ((2, 7), "bishop", "white"),
            ((5, 7), "bishop", "white"),

            ((3, 7), "queen", "white"),
            ((4, 7), "king", "white"),
        ]
    },
    "testing":{
        "players": ("white", "black"),
        "dimensions": (8, 8),
        "tile_zero": -1,
        "pieces":[
            ((0, 1), "pawn", "black"),
            ((1, 1), "pawn", "black"),
            ((2, 1), "pawn", "black"),
            ((3, 1), "pawn", "black"),
            ((4, 1), "pawn", "black"),
            ((5, 1), "pawn", "black"),
            ((6, 1), "pawn", "black"),
            ((7, 1), "pawn", "black"),

            ((3, 7), "queen", "white"),
            ((4, 7), "king", "white"),
            ((0, 7), "rook", "white"),
            ((7, 7), "rook", "white"),

            ((5, 2), "rook", "black"),

        ]
    },
}