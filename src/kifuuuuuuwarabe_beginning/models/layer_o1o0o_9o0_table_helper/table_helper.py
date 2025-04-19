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
        #usi = cshogi.move_to_usi(move)
        is_drop = cshogi.move_is_drop(move)

        if is_drop:
            #print(f"get_moving_pc_from_move: {usi=} {cshogi.move_drop_hand_piece(move)=}")
            return clazz._hand_piece_to_piece_type[cshogi.move_drop_hand_piece(move)]

        #print(f"get_moving_pc_from_move: {usi=} {cshogi.move_from_piece_type(move)=}")
        return cshogi.move_from_piece_type(move)
