class ConstantsModel():


    def __init__(self):
        self._mind = _Mind()
        self._value = _Value()
        self._out_of_termination_state = OutOfTerminationStateModel()


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
    def out_of_termination_state_const(self):
        """［終端外］です。
        """
        return self._out_of_termination_state


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


    @property
    def BIG_VALUE(self):
        """大きい数。
        """
        return 100000


    @property
    def SMALL_VALUE(self):
        """小さい数。
        """
        return -100000


    @property
    def MAYBE_EARTH_WIN_VALUE(self):
        """多分、地球勝ちの数。
        """
        return 9000


class OutOfTerminationStateModel():
    """［終端外］。
    """


    _japanese_dict = {
        0 : '未設定',
        1 : '投了局面',
        2 : '入玉宣言勝ち',
        3 : '水平線',           # 読みの最大深さ
        4 : '有力な候補手無し',
        5 : '静止',
    }


    @classmethod
    def japanese(clazz, number):
        if number in clazz._japanese_dict:
            return clazz._japanese_dict[number]
        return f"＜未定義の終端外[{number}]＞"


    @property
    def NONE(self):
        """未設定。
        """
        return 0


    @property
    def GAME_OVER(self):
        """投了局面。
        """
        return 1


    @property
    def NYUGYOKU_WIN(self):
        """入玉宣言勝ち局面時。
        """
        return 2


    @property
    def HORIZON(self):
        """水平線。
        読みの最大深さ。
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
