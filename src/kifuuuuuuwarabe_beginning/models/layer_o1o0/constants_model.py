class ConstantsModel():


    def __init__(self):
        self._mind = _Mind()
        self._value = _Value()
        self._out_of_termination = OutOfTerminationModel()


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
    def out_of_termination(self):
        """［終端外］です。
        """
        return self._out_of_termination


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


    @property
    def BETA_CUTOFF_VALUE(self):
        """ベータカットの初期値用。
        """
        return 50000


class OutOfTerminationModel():
    """［終端外］。
    """


    _japanese_dict = {
        1 : '投了',
        2 : '入玉宣言勝ち',
        3 : '読みの最大深さ',
        4 : '有力な候補手無し',
    }


    @classmethod
    def japanese(clazz, number):
        if number in clazz._japanese_dict:
            return clazz._japanese_dict[number]
        return '＜未定義の終端外＞'


    @property
    def RESIGN(self):
        """投了。
        """
        return 1


    @property
    def NYUGYOKU_WIN(self):
        """入玉宣言勝ち局面時。
        """
        return 2


    @property
    def MAX_DEPTH_BY_THINK(self):
        """読みの最大深さ。

        """
        return 3


    @property
    def NO_CANDIDATES(self):
        """有力な候補手無し。

        """
        return 4


    @property
    def QUIESCENCE(self):
        """静止。
        駒の取り合いが起こらない状態。
        """
        return 5


constants = ConstantsModel()
