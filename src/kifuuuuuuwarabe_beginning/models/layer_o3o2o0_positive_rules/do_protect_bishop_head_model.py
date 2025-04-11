import cshogi

from ..layer_o1o0 import constants, SquareModel
from ..layer_o2o0.nine_rank_side_perspective_model import NineRankSidePerspectiveModel
from ..layer_o3o1o0_negative_rules.negative_rule_model import NegativeRuleModel


class DoProtectBishopHeadModel(NegativeRuleModel):
    """TODO 訓令［ゾウの頭を守れ］

    ７六歩、７七角の２手を入れること。
    """


    def __init__(self, basketball_court_model):
        super().__init__(
                id          = 'do_protect_bishop_head',
                label       = 'ゾウの頭を守れ',
                basketball_court_model  = basketball_court_model)


    def before_move_o1o1x(self, remaining_moves, table):
        if self.is_enabled:

            np = NineRankSidePerspectiveModel(table)

            # 自ゾウが７七にいる
            if table.piece(np.masu(77)) == np.ji_pc(cshogi.BISHOP):
                # このオブジェクトを除外
                self._is_removed = True

                # 対象外
                return remaining_moves

            for i in range(len(remaining_moves))[::-1]:     # `[::-1]` - 逆順
                m = remaining_moves[i]
                mind = self.before_move(m, table)
                if mind == constants.mind.WILL_NOT:
                    del remaining_moves[i]

        return remaining_moves


    def before_move(self, move, table):
        """指す前に。
        """
        np = NineRankSidePerspectiveModel(table)

        src_sq_obj = SquareModel(cshogi.move_from(move))
        dst_sq_obj = SquareModel(cshogi.move_to(move))

        # # 自キリンが２八にいる
        # if table.piece(np.masu(28)) != np.ji_pc(cshogi.ROOK):
        #     # そうでなければ対象外
        #     return constants.mind.NOT_IN_THIS_CASE

        # 移動先は６段目ではない。
        if dst_sq_obj.rank != np.dan(6):
            # そうでなければ意志を残している
            return constants.mind.WILL

        # 動いた先は７六で、動いた駒は歩だ。
        if dst_sq_obj.sq == np.masu(76) and cshogi.piece_to_piece_type(table.piece(src_sq_obj.sq)) == cshogi.PAWN:
            # ７六に歩を突くのはＯｋ。
            return constants.mind.WILL

        # 意志なし
        return constants.mind.WILL_NOT
