class PieceValues():
    """駒の価値
    """

    # 駒種類に対応
    _values_by_pt = [
        0,  # [ 0]cshogi.NONE
        1,  # [ 1]cshogi.PAWN
        2,  # [ 2]cshogi.LANCE
        2,  # [ 3]cshogi.KNIGHT
        4,  # [ 4]cshogi.SILVER
        6,  # [ 5]cshogi.BISHOP
        8,  # [ 6]cshogi.ROOK
        5,  # [ 7]cshogi.GOLD
        99, # [ 8]cshogi.KING
        1,  # [ 9]cshogi.PROM_PAWN
        2,  # [10]cshogi.PROM_LANCE
        2,  # [11]cshogi.PROM_KNIGHT
        4,  # [12]cshogi.PROM_SILVER
        6,  # [13]cshogi.PROM_BISHOP
        8,  # [14]cshogi.PROM_ROOK
    ]

    # 先後付きの駒種類に対応
    _values_by_pc = [
        0,  # [ 0]cshogi.NONE
        1,  # [ 1]cshogi.BPAWN
        2,  # [ 2]cshogi.BLANCE
        2,  # [ 3]cshogi.BKNIGHT
        4,  # [ 4]cshogi.BSILVER
        6,  # [ 5]cshogi.BBISHOP
        8,  # [ 6]cshogi.BROOK
        5,  # [ 7]cshogi.BGOLD
        99, # [ 8]cshogi.BKING
        1,  # [ 9]cshogi.BPROM_PAWN
        2,  # [10]cshogi.BPROM_LANCE
        2,  # [11]cshogi.BPROM_KNIGHT
        4,  # [12]cshogi.BPROM_SILVER
        6,  # [13]cshogi.BPROM_BISHOP
        8,  # [14]cshogi.BPROM_ROOK
        0,  # [15]該当無し
        0,  # [16]該当無し
        -1, # [17]cshogi.WPAWN
        -2, # [18]cshogi.WLANCE
        -2, # [19]cshogi.WKNIGHT
        -4, # [20]cshogi.WSILVER
        -6, # [21]cshogi.WBISHOP
        -8, # [22]cshogi.WROOK
        -5, # [23]cshogi.WGOLD
        -99,    # [24]cshogi.WKING
        -1, # [25]cshogi.WPROM_PAWN
        -2, # [26]cshogi.WPROM_LANCE
        -2, # [27]cshogi.WPROM_KNIGHT
        -4, # [28]cshogi.WPROM_SILVER
        -6, # [29]cshogi.WPROM_BISHOP
        -8, # [30]cshogi.WPROM_ROOK
    ]


    @classmethod
    def by_piece_type(clazz, pt):
        return clazz._values_by_pt[pt]


    @classmethod
    def by_piece(clazz, pc):
        return clazz._values_by_pc[pc]
