import cshogi

from ...layer_o1o0 import constants, SquareModel
from ...layer_o2o0.nine_rank_side_perspective_model import NineRankSidePerspectiveModel
from ..negative_rule_model import NegativeRuleModel


class DoNotDropPieceModel(NegativeRuleModel):
    """号令［駒を打つな］
    """


    def __init__(self, basketball_court_model):
        super().__init__(
                id          = 'do_not_drop_piece',
                label       = '駒を打つな',
                basketball_court_model  = basketball_court_model)


    def _on_node_exit_negative(self, move, table):
        """指す前に。
        """
        
        if not cshogi.move_is_drop(move):           # ［打］でなければ。
            return constants.mind.NOT_IN_THIS_CASE  # 対象外。

        # 意志無し。
        return constants.mind.WILL_NOT
