class Constants():


    def __init__(self):
        self._mind = _Mind()
        self._value = _Value()


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
    """


    @property
    def GAME_OVER(self):
        return -100001


    @property
    def NYUGYOKU_WIN(self):
        return 100002


    @property
    def CHECKMATE(self):
        return 100003


    @property
    def STALEMATE(self):
        return -100004


constants = Constants()
