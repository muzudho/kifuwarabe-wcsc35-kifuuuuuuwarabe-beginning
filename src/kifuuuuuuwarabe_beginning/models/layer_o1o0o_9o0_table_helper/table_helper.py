import cshogi


class TableHelper:

    
    _hand_piece_to_piece_type = {
        cshogi.HPAWN    : cshogi.PAWN,
        cshogi.HLANCE   : cshogi.LANCE,
        cshogi.HKNIGHT  : cshogi.KNIGHT,
        cshogi.HSILVER  : cshogi.SILVER,
        cshogi.HGOLD    : cshogi.GOLD,
        cshogi.HBISHOP  : cshogi.BISHOP,
        cshogi.HROOK    : cshogi.ROOK}


    @classmethod
    def get_moving_pt_from_move(clazz, move):
        """［動かした駒の種類］取得。

        指し手情報（move）から算出できるので、現局面の情報は不要。
        """
        is_drop = cshogi.move_is_drop(move)

        if is_drop:
            return clazz._hand_piece_to_piece_type[cshogi.move_drop_hand_piece(move)]

        return cshogi.move_from_piece_type(move)
