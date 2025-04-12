import cshogi

from ..layer_o1o0 import constants, SquareModel
from ..layer_o2o0.nine_rank_side_perspective_model import NineRankSidePerspectiveModel
from .negative_rule_model import NegativeRuleModel


class DoNotMoveRightLanceModel(NegativeRuleModel):
    """号令［右のイノシシは動くな］
    ［右のイノシシは止まる］意志
    """


    def __init__(self, basketball_court_model):
        super().__init__(
                id          = 'do_not_move_right_lance',
                label       = '右のイノシシは動くな',
                basketball_court_model  = basketball_court_model)


    def before_branches_o1o1x(self, remaining_moves, table):
        if self.is_enabled:
            np = NineRankSidePerspectiveModel(table)

            # 自ライオンが２八にいる
            if table.piece(np.masu(28)) == np.ji_pc(cshogi.KING):
                # （処理を行わず）このオブジェクトを除外
                self._is_removed = True
            
            else:
                for i in range(len(remaining_moves))[::-1]:     # `[::-1]` - 逆順
                    m = remaining_moves[i]
                    mind = self._before_move_nrm(m, table)
                    if mind == constants.mind.WILL_NOT:
                        del remaining_moves[i]

        return remaining_moves


    def _before_move_nrm(self, move, table):
        """指す前に。
        """

        np = NineRankSidePerspectiveModel(table)

        src_sq_obj = SquareModel(cshogi.move_from(move))

        # いのしし以外なら対象外
        if cshogi.move_from_piece_type(move) not in [cshogi.LANCE]:
            return constants.mind.NOT_IN_THIS_CASE

        # １筋の駒が動いたら意志無し
        #print(f'★ ＤoNotMoveRightLance._before_move_nrm(): {src_sq_obj.file=} {np.suji(1)=}')
        if src_sq_obj.file == np.suji(1):
            return constants.mind.WILL_NOT

        # それ以外は意志有り
        return constants.mind.WILL
