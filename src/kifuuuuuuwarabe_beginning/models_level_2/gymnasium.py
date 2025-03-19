from ..models.table_access_object import PieceValueTAO


class Gymnasium():
    """体育館。きふわらべはなぜか体育館で将棋をしている。
    """


    def __init__(self, table):
        """初期化します。
        """

        # 盤へアクセスする関連のオブジェクト
        self._piece_value_tao = PieceValueTAO(table = table)

        # ９段目に近い方の対局者から見た駒得評価値。
        self._nine_rank_side_value = 0


    @property
    def piece_value_tao(self):
        return self._piece_value_tao


    @property
    def nine_rank_side_value(self):
        """９段目に近い方の対局者から見た駒得評価値。
        """
        return self._nine_rank_side_value


    @nine_rank_side_value.setter
    def nine_rank_side_value(self, value):
        self._nine_rank_side_value = value


    def on_new_game(self):
        self._nine_rank_side_value = 0  # ９段目に近い方の対局者から見た駒得評価値。
