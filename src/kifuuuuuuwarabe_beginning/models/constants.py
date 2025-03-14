class Constants():


    def __init__(self):
        self._mind = _Mind()


    @property
    def mind(self):
        """盤の面積です。
        """

        return self._mind


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
        return 0


    @property
    def WILL_NOT(self):
        return 1


    @property
    def WILL(self):
        return 2



constants = Constants()
