import cshogi

from ..layer_o1o0o_9o0_table_helper import TableHelper
from ..layer_o1o0o1o0_human import HumanPresentableMoveModel


class FrontwardsPlotModel(): # TODO Rename PathFromRoot
    """木構造の根から葉に向かって指し手を追加していきます。（前向き）
    """


    def __init__(self):
        self._move_list = []        # 指し手のリスト。


    def append_move(self, move):
        """指し手の追加。
        """
        self._move_list.append(move)


    def pop_move(self):
        """最後の指し手の削除。
        """
        self._move_list.pop()


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

        len_of_move_list = len(self._move_list)
        for layer_no in range(0, len_of_move_list):
            move = self._move_list[layer_no]
            moving_pt = TableHelper.get_moving_pt_from_move(move)

            move_str = cshogi.move_to_usi(move)
            # 指し手のUSI表記を独自形式に変更。
            #move_str = HumanPresentableMoveModel.from_move(move=move, moving_pt=moving_pt, is_mars=is_mars, is_gote=is_gote).stringify()

            tokens.append(move_str)
        
        return ','.join(tokens)
