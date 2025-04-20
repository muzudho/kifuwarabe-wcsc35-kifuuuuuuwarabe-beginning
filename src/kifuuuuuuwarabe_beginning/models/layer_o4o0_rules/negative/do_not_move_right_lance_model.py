import cshogi

from ...layer_o1o0 import constants, SquareModel
from ...layer_o1o0o_9o0_table_helper import TableHelper
from ...layer_o2o0.nine_rank_side_perspective_model import NineRankSidePerspectiveModel
from ..negative_rule_model import NegativeRuleModel


class DoNotMoveRightLanceModel(NegativeRuleModel):
    """号令［右のイノシシは動くな］
    ［右のイノシシは止まる］意志
    """


    def __init__(self, basketball_court_model):
        super().__init__(
                id          = 'do_not_move_right_lance',
                label       = '右のイノシシは動くな',
                basketball_court_model  = basketball_court_model)


    def _remove_rule_before_branches_nrm(self, remaining_moves, table):
        """枝前削除条件。
        真なら、このルールをリストから除外します。
        """
        np = NineRankSidePerspectiveModel(table)

        # （事前リムーブ分岐）自ライオンが２八にいる
        return table.piece(np.masu(28)) == np.ji_pc(cshogi.KING)


    def _before_move_nrm(self, move, table):
        """指す前に。
        """

        np = NineRankSidePerspectiveModel(table)
        moving_pt = TableHelper.get_moving_pt_from_move(move)
        src_sq_obj = SquareModel(cshogi.move_from(move))

        if moving_pt != cshogi.LANCE:               # いのしし以外なら。
            return constants.mind.NOT_IN_THIS_CASE  # 対象外。

        # １筋の駒が動いたら意志無し
        #print(f'★ ＤoNotMoveRightLance._before_move_nrm(): {src_sq_obj.file=} {np.suji(1)=}')
        if src_sq_obj.file == np.suji(1):
            return constants.mind.WILL_NOT

        # それ以外は意志有り
        return constants.mind.WILL
