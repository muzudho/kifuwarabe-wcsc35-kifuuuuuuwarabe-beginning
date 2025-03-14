class Constants():


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


constants = Constants()
