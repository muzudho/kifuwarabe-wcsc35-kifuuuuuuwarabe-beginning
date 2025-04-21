import cshogi

from ...layer_o1o0 import constants, SquareModel
from ...layer_o2o0.nine_rank_side_perspective_model import NineRankSidePerspectiveModel
from ..negative_rule_model import NegativeRuleModel


class DoNotDropRookInOwnCampModel(NegativeRuleModel):
    """号令［自陣に飛車打つな］
    """


    def __init__(self, basketball_court_model):
        super().__init__(
                id          = 'do_not_drop_rook_in_own_camp_model',
                label       = '自陣に飛車打つな',
                basketball_court_model  = basketball_court_model)


    def _before_move_nrm(self, move, table):
        """指す前に。
        """
        
        if not cshogi.move_is_drop(move):           # ［打］でなければ。
            return constants.mind.NOT_IN_THIS_CASE  # 対象外。

        if cshogi.move_drop_hand_piece(move) != cshogi.HROOK:    # キリンでなければ。
            return constants.mind.NOT_IN_THIS_CASE              # 対象外。

        np = NineRankSidePerspectiveModel(table)
        dst_sq_obj = SquareModel(cshogi.move_to(move))

        (a, b) = np.swap(np.dan(7), dst_sq_obj.rank)    # ７段目より上に打つ手なら。
        if a < b:
            return constants.mind.NOT_IN_THIS_CASE  # 対象外。

        # 意志無し。
        return constants.mind.WILL_NOT
