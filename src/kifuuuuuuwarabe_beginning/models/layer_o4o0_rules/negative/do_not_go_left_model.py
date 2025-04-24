import cshogi

from ...layer_o1o0 import constants, SquareModel
from ...layer_o1o0o_9o0_table_helper import TableHelper
from ...layer_o2o0.nine_rank_side_perspective_model import NineRankSidePerspectiveModel
from ..negative_rule_model import NegativeRuleModel


class DoNotGoLeftModel(NegativeRuleModel):
    """号令［左へ行くな］
    ［右へ行く］意志
    """


    def __init__(self, basketball_court_model):
        super().__init__(
                id          = 'do_not_go_left',
                label       = '左へ行くな',
                basketball_court_model  = basketball_court_model)


    def _on_node_exit_negative(self, move, table):
        """指す前に。
        """
        np = NineRankSidePerspectiveModel(table)
        moving_pt = TableHelper.get_moving_pt_from_move(move)
        src_sq_obj = SquareModel(cshogi.move_from(move))
        dst_sq_obj = SquareModel(cshogi.move_to(move))

        # ライオンなら、以左には行くな。
        if moving_pt == cshogi.KING:
            # 移動先が右なら意志あり
            (a, b) = np.swap(dst_sq_obj.file, src_sq_obj.file)
            if a < b:
                return constants.mind.WILL

            # それ以外は意志なし
            return constants.mind.WILL_NOT

        # イヌ、ネコなら
        if moving_pt in [cshogi.GOLD, cshogi.SILVER]:
            # ６筋位左にある駒は対象外
            (a, b) = np.swap(src_sq_obj.file, np.suji(6))
            if a >= b:
                return constants.mind.NOT_IN_THIS_CASE

            # 移動先が同筋位右なら意志あり
            (a, b) = np.swap(dst_sq_obj.file, src_sq_obj.file)
            if a <= b:
                return constants.mind.WILL

            # それ以外は意志なし
            return constants.mind.WILL_NOT

        # それ以外なら対象外
        return constants.mind.NOT_IN_THIS_CASE
