import cshogi

from ...layer_o1o0 import constants, SquareModel
from ...layer_o2o0.nine_rank_side_perspective_model import NineRankSidePerspectiveModel
from ..positive_rule_model import PositiveRuleModel


class DoProtectBishopHeadModel(PositiveRuleModel):
    """訓令［ゾウの頭を守れ］

    ７六歩、７七角の２手を入れること。
    """


    def __init__(self, basketball_court_model):
        super().__init__(
                id          = 'do_protect_bishop_head',
                label       = 'ゾウの頭を守れ',
                basketball_court_model  = basketball_court_model)


    ##############################
    # MARK: オーバーライドメソッド
    ##############################

    def _remove_rule_on_node_entry_positive(self, remaining_moves, table):
        """枝前削除条件。
        真なら、このルールをリストから除外します。
        """
        np = NineRankSidePerspectiveModel(table)

        # 事前ケース分岐）［自ゾウが７七にいる］ならこのルールを消す。
        return table.piece(np.masu(77)) == np.ji_pc(cshogi.BISHOP)


    def _on_node_entry_positive(self, remaining_moves, table):
        """どの枝も指す前に。

        Returns
        -------
        moves_to_pickup : list<int>
            ピックアップした指し手。
        """

        np = NineRankSidePerspectiveModel(table)

        # ［ヒヨコ on ６六］が有るか確認。
        self._is_hiyoko_on_66 = table.piece(np.masu(66)) == np.ji_pc(cshogi.PAWN)
        # ［ヒヨコ on ７六］が有るか確認。
        self._is_hiyoko_on_76 = table.piece(np.masu(76)) == np.ji_pc(cshogi.PAWN)
        # ［歩 not on ３三］か確認。
        self._is_pawn_not_on_33 = table.piece(np.masu(33)) != np.aite_pc(cshogi.PAWN)

        return []


    def _on_node_exit_positive(self, move, table):
        """指す前にこの手に決める。

        Returns
        -------
        is_better_move : bool
            指させたい手なら真。
        """
        np = NineRankSidePerspectiveModel(table)

        src_sq_obj = SquareModel(cshogi.move_from(move))
        dst_sq_obj = SquareModel(cshogi.move_to(move))
        moving_pc = table.piece(src_sq_obj.sq)

        # これが［７六ヒヨコ］なら、選ぶ。
        if moving_pc == np.ji_pc(cshogi.PAWN) and dst_sq_obj.sq == np.masu(76):
            return True

        # これが［６六ヒヨコ］なら。
        if moving_pc == np.ji_pc(cshogi.PAWN) and dst_sq_obj.sq == np.masu(66):
            # ［ヒヨコ on ７六］、［歩 not on ３三］なら、選ぶ。
            if self._is_hiyoko_on_76 and self._is_pawn_not_on_33:
                return True
            return False

        # これが［７七ゾウ］なら。（［７六歩］を突いていなければ、そもそもこの手は存在しない）
        if moving_pc == np.ji_pc(cshogi.BISHOP) and dst_sq_obj.sq == np.masu(77):
            # not［歩 not on ３三］または［ヒヨコ on ６六］なら、選ぶ。
            if not self._is_pawn_not_on_33 or self._is_hiyoko_on_66:
                return True
            return False

        # それ以外は無視。
        return False


    ##############################
    # MARK: オーバーライドメソッド
    ##############################

    def _remove_rule_on_node_entry_positive(self, remaining_moves, table):
        """枝前削除条件。
        真なら、このルールをリストから除外します。
        """

        np = NineRankSidePerspectiveModel(table)

        # 事前ケース分岐）［自ゾウが７七にいる］ならこのルールを消す。
        return table.piece(np.masu(77)) == np.ji_pc(cshogi.BISHOP)
