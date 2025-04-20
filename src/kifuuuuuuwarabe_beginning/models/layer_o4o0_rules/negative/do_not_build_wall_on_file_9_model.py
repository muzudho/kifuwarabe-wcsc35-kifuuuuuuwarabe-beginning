import cshogi

from ....logics.layer_o1o0.helper import Helper
from ...layer_o1o0 import constants, PieceModel, SquareModel
from ...layer_o1o0o_9o0_table_helper import TableHelper
from ...layer_o2o0.nine_rank_side_perspective_model import NineRankSidePerspectiveModel
from ..negative_rule_model import NegativeRuleModel


class DoNotBuildWallOnFile9Model(NegativeRuleModel):
    """号令［９筋に壁を作るな］

    意図：９間飛車を禁止している。
    """


    def __init__(self, basketball_court_model):
        super().__init__(
                id          = 'do_not_build_wall_on_file_9',
                label       = '９筋に壁を作るな',
                basketball_court_model  = basketball_court_model)


    def _before_move_nrm(self, move, table):
        """指す前に。
        """
        np = NineRankSidePerspectiveModel(table)
        dst_sq_obj = SquareModel(cshogi.move_to(move))

        if dst_sq_obj.rank not in [np.dan(8), np.dan(9)]:   # ８段目、９段目以外に移動する手なら。
            return constants.mind.NOT_IN_THIS_CASE          # 対象外。

        if dst_sq_obj.file != np.suji(9):   # ９筋目以外に移動する手なら。
            return constants.mind.NOT_IN_THIS_CASE          # 対象外。

        # ９八、９九の両方に自駒があるか？
        pc98 = table.piece(np.masu(98))
        pc99 = table.piece(np.masu(99))
        if pc98 != cshogi.NONE and PieceModel.turn(pc98) == table.turn and pc99 != cshogi.NONE and PieceModel.turn(pc99) == table.turn:
            # 意志無し。
            return constants.mind.WILL_NOT

        # 対象外。
        return constants.mind.NOT_IN_THIS_CASE
