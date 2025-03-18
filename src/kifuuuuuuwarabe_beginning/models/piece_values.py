class PieceValues():
    """駒の価値
    """

    # 駒種類に対応
    _values = [
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


    @classmethod
    def by_piece_type(clazz, pt):
        return clazz._values[pt]
