import cshogi

from ...layer_o1o0 import constants, SquareModel
from ...layer_o2o0.nine_rank_side_perspective_model import NineRankSidePerspectiveModel
from ..negative_rule_model import NegativeRuleModel


class DoNotMoveLeftLanceModel(NegativeRuleModel):
    """号令［左のイノシシは動くな］
    ［左のイノシシは止まる］意志
    """


    def __init__(self, basketball_court_model):
        super().__init__(
                id          = 'do_not_move_left_lance',
                label       = '左のイノシシは動くな',
                basketball_court_model  = basketball_court_model)


    def _before_move_nrm(self, move, table):
        """指す前に。
        """

        np = NineRankSidePerspectiveModel(table)

        src_sq_obj = SquareModel(cshogi.move_from(move))

        # いのしし以外なら対象外
        if cshogi.move_from_piece_type(move) not in [cshogi.LANCE]:
            return constants.mind.NOT_IN_THIS_CASE

        # ９筋の駒が動いたら意志無し
        #print(f'★ ＤoNotMoveLeftLance._before_move_nrm(): {src_sq_obj.file=} {np.suji(9)=}')
        if src_sq_obj.file == np.suji(9):
            return constants.mind.WILL_NOT

        # それ以外は意志有り
        return constants.mind.WILL
