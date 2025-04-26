import cshogi

from ..layer_o1o0o1o0_japanese import JapaneseMoveModel


class FrontwardsPlotModel(): # TODO Rename PathFromRoot
    """木構造の根から葉に向かって指し手を追加していきます。（前向き）
    """


    def __init__(self, is_gote_at_first):
        self._is_gote_at_first = is_gote_at_first   # 最初の要素は後手か？
        self._move_list = []        # 指し手のリスト。
        self._cap_list = []         # 取った駒種類のリスト。
        #self._piece_exchange_value_list_on_earth


    @property
    def is_mars_at_peek(self):
        """最後の要素は火星か？
        """
        if len(self._move_list) % 2 == 0:
            return False
        return True


    @property
    def is_gote_at_peek(self):
        """最後の要素は後手か？
        """
        if len(self._move_list) % 2 == 0:
            return not self.is_gote_at_first
        return self.is_gote_at_first


    def append_move_from_front(self, move, cap_pt):
        """指し手の追加。
        """
        self._move_list.append(move)
        self._cap_list.append(cap_pt)


    def pop_move(self):
        """最後の指し手の削除。
        """
        self._move_list.pop()
        self._cap_list.pop()


    def equals_move_usi_list(self, move_usi_list):
        """完全一致判定。
        """
        usi_list = []
        for move in self._move_list:
            usi_list.append(cshogi.move_to_usi(move))

        return usi_list == move_usi_list


    def stringify(self):
        """文字列化。
        """
        tokens = []

        is_mars = self.is_mars_at_peek
        is_gote = self.is_gote_at_peek

        len_of_move_list = len(self._move_list)
        for layer_no in range(0, len_of_move_list):
            move = self._move_list[layer_no]
            cap_pt = self._cap_list[layer_no]

            # 指し手のUSI表記を独自形式に変更。
            move_jp_str = JapaneseMoveModel.from_move(
                    move    = move,
                    cap_pt  = cap_pt,
                    is_mars = is_mars,
                    is_gote = is_gote).stringify()

            tokens.append(move_jp_str)

            # 手番交代
            is_mars = not is_mars
            is_gote = not is_gote

        return ','.join(tokens)
