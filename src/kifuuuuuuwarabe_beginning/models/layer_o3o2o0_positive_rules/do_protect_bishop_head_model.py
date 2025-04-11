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


    def before_branches_o1o1x(self, remaining_moves, table):
        """どの手も指す前に。

        Returns
        -------
        moves_to_pickup : list<int>
            ピックアップした指し手。
        """

        moves_to_pickup = []

        if self.is_enabled:
            np = NineRankSidePerspectiveModel(table)

            # ［自ゾウが７七にいる］ならこのルールを消す。
            if table.piece(np.masu(77)) == np.ji_pc(cshogi.BISHOP):
                # このオブジェクトを除外
                self._is_removed = True

                # 対象外
                return []

            for i in range(len(remaining_moves))[::-1]:     # `[::-1]` - 逆順
                m = remaining_moves[i]
                if self.is_better_move_before_branches(m, table):
                    moves_to_pickup.append(m)

        return moves_to_pickup


    def is_better_move_before_branches(self, move, table):
        """指す前にこの手に決める。
        """
        np = NineRankSidePerspectiveModel(table)

        src_sq_obj = SquareModel(cshogi.move_from(move))
        dst_sq_obj = SquareModel(cshogi.move_to(move))

        # ［７七角］があれば、それを選ぶ。
        if table.piece(src_sq_obj.sq) == np.ji_pc(cshogi.BISHOP) and dst_sq_obj.sq == np.masu(77):
            return True

        # ［７六歩］があれば、それを選ぶ。
        if table.piece(src_sq_obj.sq) == np.ji_pc(cshogi.PAWN) and dst_sq_obj.sq == np.masu(76):
            return True

        # それ以外は無視
        return False
