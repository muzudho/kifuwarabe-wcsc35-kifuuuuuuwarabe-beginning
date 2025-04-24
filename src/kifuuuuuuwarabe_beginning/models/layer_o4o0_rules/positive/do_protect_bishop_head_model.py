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

        # ［７六歩］が有るか確認。
        self._is_76hiyoko = False

        for move in remaining_moves:
            src_sq_obj = SquareModel(cshogi.move_from(move))
            dst_sq_obj = SquareModel(cshogi.move_to(move))
            if table.piece(src_sq_obj.sq) == np.ji_pc(cshogi.PAWN) and dst_sq_obj.sq == np.masu(76):
                self._is_76hiyoko = True
                break

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

        # これが［７六歩］なら、選ぶ。
        if table.piece(src_sq_obj.sq) == np.ji_pc(cshogi.PAWN) and dst_sq_obj.sq == np.masu(76):
            return True

        # これが［７七角］なら、選ぶ。（［７六歩］を突いていなければ、そもそもこの手は存在しない）
        if table.piece(src_sq_obj.sq) == np.ji_pc(cshogi.BISHOP) and dst_sq_obj.sq == np.masu(77):
            return True
        
        # ［７六歩］が指せない局面で。（既に［７六歩］を突いていることを想定）
        if not self._is_76hiyoko:
            # これが［６六歩］なら、選ぶ。
            if table.piece(src_sq_obj.sq) == np.ji_pc(cshogi.PAWN) and dst_sq_obj.sq == np.masu(66):
                return True

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
