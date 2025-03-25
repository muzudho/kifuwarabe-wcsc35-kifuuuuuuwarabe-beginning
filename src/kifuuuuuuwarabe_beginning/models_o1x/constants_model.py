class ConstantsModel():


    def __init__(self):
        self._mind = _Mind()
        self._value = _Value()
        self._declaration = _Declaration()


    @property
    def mind(self):
        """盤の面積です。
        """
        return self._mind


    @property
    def value(self):
        """評価値です。
        """
        return self._value


    @property
    def declaration(self):
        """［宣言］です。
        """
        return self._declaration


    @property
    def BOARD_AREA(self):
        """盤の面積です。
        """

        return 81   # 9 * 9


    @property
    def PIECE_STAND_SQ(self):
        """駒台を指すマス番号です。
        """

        global constants
        return constants.BOARD_AREA


class _Mind():
    """心
    """


    @property
    def NOT_IN_THIS_CASE(self):
        return 1


    @property
    def WILL_NOT(self):
        return 2


    @property
    def WILL(self):
        return 3


class _Value():
    """評価値。
    例： 10001
        abbcc
        a : 勝敗状態。
            -1: GAME OVER（投了）
             2: 入玉宣言勝ち
             3: １手詰め
            -4: 駒を取る手が無し
        b : ゼロが２個並ぶ
        c : 駒得の点数。
    """


    @property
    def ZERO(self):
        return 0


    @property
    def GAME_OVER(self):
        """［投了］
        """
        return -10000


    @property
    def NYUGYOKU_WIN(self):
        """［入玉宣言勝ち］
        """
        return 20000


    @property
    def CHECKMATE(self):
        """［一手詰め］
        """
        return 30000


    @property
    def NOTHING_CAPTURE_MOVE(self):
        """［駒を取る手が無し］
        """
        return -40000


class _Declaration():
    """［宣言］。
    """


    @property
    def NONE(self):
        """宣言ではありません。
        """
        return 0


    @property
    def RESIGN(self):
        """投了。
        """
        return 1


    @property
    def NYUGYOKU_WIN(self):
        """入玉宣言局面時。
        """
        return 2


constants = ConstantsModel()
