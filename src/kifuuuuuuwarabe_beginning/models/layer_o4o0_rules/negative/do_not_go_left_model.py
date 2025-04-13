import cshogi

from ...layer_o1o0 import constants, SquareModel
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


    def _before_move_nrm(self, move, table):
        """指す前に。
        """

        np = NineRankSidePerspectiveModel(table)

        src_sq_obj = SquareModel(cshogi.move_from(move))
        dst_sq_obj = SquareModel(cshogi.move_to(move))

        # ライオンなら、以左には行くな。
        if cshogi.move_from_piece_type(move) == cshogi.KING:
            # 移動先が右なら意志あり
            e1 = np.swap(dst_sq_obj.file, src_sq_obj.file)
            if e1[0] < e1[1]:
                return constants.mind.WILL

            # それ以外は意志なし
            return constants.mind.WILL_NOT

        # イヌ、ネコなら
        if cshogi.move_from_piece_type(move) in [cshogi.GOLD, cshogi.SILVER]:
            # ６筋位左にある駒は対象外
            e1 = np.swap(src_sq_obj.file, np.suji(6))
            if e1[0] >= e1[1]:
                return constants.mind.NOT_IN_THIS_CASE

            # 移動先が同筋位右なら意志あり
            e1 = np.swap(dst_sq_obj.file, src_sq_obj.file)
            if e1[0] <= e1[1]:
                return constants.mind.WILL

            # それ以外は意志なし
            return constants.mind.WILL_NOT

        # それ以外なら対象外
        return constants.mind.NOT_IN_THIS_CASE
