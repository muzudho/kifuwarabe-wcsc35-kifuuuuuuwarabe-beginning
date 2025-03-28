import cshogi


class PieceMovedModel():
    """１手指した直後に記憶しておく様々な情報

    NOTE 局面の重複を調べるために、０手の SFEN をリストで持ちたい
    """


    def __init__(self, move, sfen_with_0_moves):
        """
        Parameters
        ----------
        move : int
            ［指し手］
        """
        self._move = move
        self._sfen_with_0_moves = sfen_with_0_moves

        # TODO 同形局面反復回数
        self._number_of_repetition = 0


    @property
    def move(self):
        return self._move


    @property
    def sfen_with_0_moves(self):
        """同形反復回数を数えるのに利用する
        """
        return self._sfen_with_0_moves


    @property
    def number_of_repetition(self):
        """同形反復回数
        """
        return self._number_of_repetition


    def dump(self):
        return f"{cshogi.move_to_usi(self._move)=} {self._sfen_with_0_moves=} {self._number_of_repetition=}"
