class NoteBook():


    def __init__(self):
        """初期化します。
        """

        # ９段目に近い方の対局者から見た駒得評価値。
        self._nine_rank_side_value = 0


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
