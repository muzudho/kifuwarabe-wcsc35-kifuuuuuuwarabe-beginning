import cshogi

from ..layer_o1o0 import constants, SquareModel
from ..layer_o2o0.nine_rank_side_perspective_model import NineRankSidePerspectiveModel
from .negative_rule_model import NegativeRuleModel


class DoNotMoveRookModel(NegativeRuleModel):
    """号令［キリンは動くな］
    ［きりんは止まる］意志

    NOTE 初期状態は［アイドリング］で始まり、飛車を振った後に有効化します
    """


    def __init__(self, basketball_court_model):
        super().__init__(
                id      = 'do_not_move_rook',
                label   = 'キリンは動くな',
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
                    mind = self._before_move(m, table)
                    if mind == constants.mind.WILL_NOT:
                        del remaining_moves[i]

        return remaining_moves


    def _after_best_moving_in_idling_nrm(self, move, table):
        """（アイドリング中の号令について）指す手の確定時。
        """

        if self.is_enabled:
            np = NineRankSidePerspectiveModel(table)

            src_sq_obj = SquareModel(cshogi.move_from(move))
            dst_sq_obj = SquareModel(cshogi.move_to(move))

            # キリン以外なら対象外。
            if cshogi.move_from_piece_type(move) != cshogi.ROOK:
                return

            # キリンの移動先が異筋なら、この号令を有効化します。
            e1 = np.swap(dst_sq_obj.file, src_sq_obj.file)
            if e1[0] != e1[1]:
                print(f'★ ｏn_best_move_played: {self.label=} 有効化')
                self._is_activate = True

            #     # キリンの移動先が異段なら、この号令は削除します。
            #     e1 = cmp.swap(dst_sq_obj.rank, src_sq_obj.rank)
            #     if e1[0] != e1[1]:
            #         self._is_removed = True


    ####################
    # MARK: サブルーチン
    ####################


    def _before_move(self, move, table):
        """指す前に。
        """

        # キリン以外なら対象外
        if cshogi.move_from_piece_type(move) not in [cshogi.ROOK]:
            return constants.mind.NOT_IN_THIS_CASE

        # # 移動先が異段なら意志あり
        # e1 = cmp.swap(dst_sq_obj.rank, src_sq_obj.rank)
        # if e1[0] != e1[1]:
        #     return constants.mind.WILL

        # それ以外は意志なし
        return constants.mind.WILL_NOT
