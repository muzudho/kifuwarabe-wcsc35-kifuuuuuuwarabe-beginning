import cshogi

from ...layer_o1o0 import constants, SquareModel
from ...layer_o2o0.nine_rank_side_perspective_model import NineRankSidePerspectiveModel
from ..negative_rule_model import NegativeRuleModel


class DoNotBreakFamousFenceModel(NegativeRuleModel):
    """訓令［名の有る囲いを崩すな］
    ［名の有る囲いを保つ］意志
    """


    def __init__(self, basketball_court_model):
        super().__init__(
                id          = 'do_not_break_famous_fence',
                label       = '名の有る囲いを崩すな',
                basketball_court_model  = basketball_court_model)


    def _on_node_exit_negative(self, move, table):
        """指す前に。
        """
        np = NineRankSidePerspectiveModel(table)

        src_sq_obj = SquareModel(cshogi.move_from(move))

        # ［大住囲い］
        if (
                np.ji_pc(cshogi.KING) == table.piece(np.masu(38))     # 自ライオンが［３八］
            and np.ji_pc(cshogi.GOLD) == table.piece(np.masu(48))     # 自イヌが［４八］
            and np.ji_pc(cshogi.SILVER) == table.piece(np.masu(39))   # 自ネコが［３九］
            ):
            if src_sq_obj.sq in [np.masu(38), np.masu(48), np.masu(39)]:
                # 順法の意志無し
                return constants.mind.WILL_NOT

            # 順法の意志有り
            return constants.mind.WILL
        
        # 対象外
        return constants.mind.NOT_IN_THIS_CASE
