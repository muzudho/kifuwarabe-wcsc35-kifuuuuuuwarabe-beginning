import cshogi

from ...layer_o1o0 import constants, SquareModel
from ...layer_o1o0o_9o0_table_helper import TableHelper
from ...layer_o2o0.nine_rank_side_perspective_model import NineRankSidePerspectiveModel
from ..negative_rule_model import NegativeRuleModel


class DoNotMoveUntilRookMovesModel(NegativeRuleModel):
    """号令［キリンが動くまで動くな］
    ［飛車道を開ける］意志
    """


    def __init__(self, basketball_court_model):
        super().__init__(
                id          = 'do_not_move_until_rook_moves',
                label       = 'キリンが動くまで動くな',
                basketball_court_model  = basketball_court_model)


    def _on_node_exit_negative(self, move, table):
        """指す前に。
        """
        np = NineRankSidePerspectiveModel(table)
        moving_pt = TableHelper.get_moving_pt_from_move(move)
        dst_sq_obj = SquareModel(cshogi.move_to(move))

        # キリンが２八にいないなら。
        if table.piece(np.masu(28)) != np.ji_pc(cshogi.ROOK):
            # 対象外。
            return constants.mind.NOT_IN_THIS_CASE

        # 移動先は８段目ではないなら。
        if dst_sq_obj.rank != np.dan(8):
            # 対象外。
            return constants.mind.NOT_IN_THIS_CASE

        # 動かした駒がキリンなら。
        if moving_pt == cshogi.ROOK:
            # 対象外。
            return constants.mind.NOT_IN_THIS_CASE

        # 動かした駒がライオン、イヌ、ネコのいずれかなら
        if moving_pt in [cshogi.KING, cshogi.GOLD, cshogi.SILVER]:
            # 意志無し
            return constants.mind.WILL_NOT

        # 象が７７象、６８象と移動して飛車道を塞ぐのも困る。
        if moving_pt == cshogi.BISHOP:
            (a, b) = np.swap(np.suji(6), dst_sq_obj.file)
            if a <= b:
                # 意志無し
                return constants.mind.WILL_NOT

        # # 動かした駒が金なら
        # if moving_pt == cshogi.GOLD:
        #     # ５筋以右にある金なら
        #     (a, b) = cmp.swap(src_sq_obj.file, np.suji(5))
        #     if a <= b:
        #         # 動かしたら意志なし
        #         return constants.mind.WILL_NOT

        #     # それ以外の金なら、左の方以外に動かしたら意志なし
        #     (a, b) = cmp.swap(src_sq_obj.file, dst_sq_obj.file)
        #     if a < b:
        #         return constants.mind.WILL_NOT
            
        #     # 左の方に動かしたのなら、まあ、対象外
        #     return constants.mind.NOT_IN_THIS_CASE

        # # 動かした駒が銀なら
        # if moving_pt == cshogi.SILVER:
        #     # ５筋以右にある銀を動かしたなら
        #     (a, b) = cmp.swap(src_sq_obj.file, np.suji(5))
        #     if a <= b:
        #         # 意志なし
        #         return constants.mind.WILL_NOT

        #     # それ以外の銀を、元位置より右の方に動かしたら意志なし
        #     (a, b) = cmp.swap(src_sq_obj.file, dst_sq_obj.file)
        #     if a > b:
        #         return constants.mind.WILL_NOT
            
        #     # 位左の方に動かしたのなら、まあ、対象外
        #     return constants.mind.NOT_IN_THIS_CASE

        # それ以外なら意志を残している
        return constants.mind.WILL
