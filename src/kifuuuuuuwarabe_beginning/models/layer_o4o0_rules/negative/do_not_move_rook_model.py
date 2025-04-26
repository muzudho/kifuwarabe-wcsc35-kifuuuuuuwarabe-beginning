import cshogi

from ...layer_o1o0 import constants, SquareModel
from ...layer_o1o0o_9o0_table_helper import TableHelper
from ...layer_o2o0.nine_rank_side_perspective_model import NineRankSidePerspectiveModel
from ..negative_rule_model import NegativeRuleModel


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


    def _remove_rule_on_node_entry_negative(self, remaining_moves, table):
        """ノード来訪時削除条件。
        真なら、このルールをリストから除外します。
        """
        np = NineRankSidePerspectiveModel(table)

        # （事前リムーブ分岐）自ライオンが２八にいる
        return table.piece(np.masu(28)) == np.ji_pc(cshogi.KING)


    def _after_best_moving_in_idling_nrm(self, move, table):
        """（アイドリング中の号令について）指す手の確定時。
        """

        if not self.is_enabled:
            return

        #np = NineRankSidePerspectiveModel(table)
        moving_pt = TableHelper.get_moving_pt_from_move(move)
        src_sq_obj = SquareModel(cshogi.move_from(move))
        dst_sq_obj = SquareModel(cshogi.move_to(move))

        if moving_pt != cshogi.ROOK:    # キリン以外なら。
            return                      # 対象外。

        # キリンが異筋に移動したあと、この号令を有効化します。
        if src_sq_obj.file != dst_sq_obj.file:
            self._is_activate = True


    ####################
    # MARK: サブルーチン
    ####################

    def _on_node_exit_negative(self, move, table):
        """指す前に。
        """

        moving_pt = TableHelper.get_moving_pt_from_move(move)

        # キリン以外なら対象外
        if moving_pt != cshogi.ROOK:
            return constants.mind.NOT_IN_THIS_CASE

        # それ以外は意志なし
        return constants.mind.WILL_NOT
