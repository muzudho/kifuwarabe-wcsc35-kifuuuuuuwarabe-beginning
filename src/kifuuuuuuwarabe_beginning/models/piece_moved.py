class PieceMoved():
    """１手指した直後に記憶しておく様々な情報

    NOTE 局面の重複を調べるために、０手の SFEN をリストで持ちたい
    """


    def __init__(self, move_as_usi, sfen_with_0_moves):
        self._move_as_usi = move_as_usi
        self._sfen_with_0_moves = sfen_with_0_moves


    @property
    def move_as_usi(self):
        return self._move_as_usi


    @property
    def sfen_with_0_moves(self):
        """同形反復回数を数えるのに利用する
        """
        return self._sfen_with_0_moves
