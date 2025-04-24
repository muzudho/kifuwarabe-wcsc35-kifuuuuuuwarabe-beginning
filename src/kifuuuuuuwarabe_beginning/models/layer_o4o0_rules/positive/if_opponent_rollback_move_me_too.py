import cshogi

from ...layer_o1o0 import constants, SquareModel
from ...layer_o2o0.nine_rank_side_perspective_model import NineRankSidePerspectiveModel
from ..positive_rule_model import PositiveRuleModel


class IfOpponentRollbackMoveMeToo(PositiveRuleModel):
    """号令［相手が手を戻したら自分も戻せ］

    相手だけ得させないように。
    """


    def __init__(self, basketball_court_model):
        super().__init__(
                id          = 'if_opponent_rollback_move_me_too',
                label       = '相手が手を戻したら自分も戻せ',
                basketball_court_model  = basketball_court_model)


    ##############################
    # MARK: オーバーライドメソッド
    ##############################

    def _on_node_entry_positive(self, remaining_moves, table):
        """どの枝も指す前に。

        Returns
        -------
        moves_to_pickup : list<int>
            ピックアップした指し手。
        """

        self.is_opponent_rollback = False

        # 最終手Bと、その２つ前の手Aを取得する。
        if table.len_of_history() < 3:
            return []

        move_b                  = table.history_at(-1)
        self._my_previous_move  = table.history_at(-2)
        move_a                  = table.history_at(-3)

        # Aの移動先と、Bの移動元が一致し、かつ、Bの移動先とAの移動元が一致した場合、［手戻し］だ。
        b_src_sq_obj = SquareModel(cshogi.move_from(move_b))
        b_dst_sq_obj = SquareModel(cshogi.move_to(move_b))
        a_src_sq_obj = SquareModel(cshogi.move_from(move_a))
        a_dst_sq_obj = SquareModel(cshogi.move_to(move_a))

        if (
                a_dst_sq_obj.sq == b_src_sq_obj.sq
            and b_dst_sq_obj.sq == a_src_sq_obj.sq
        ):
            self.is_opponent_rollback = True

        return []


    def _on_node_exit_positive(self, move, table):
        """指す前にこの手に決める。

        Returns
        -------
        is_better_move : bool
            指させたい手なら真。
        """

        if not self.is_opponent_rollback:
            return False

        # 今回の手Bと、その２つ前の手Aがある。
        # Aの移動先と、Bの移動元が一致し、かつ、Bの移動先とAの移動元が一致した場合、［手戻し］だ。
        b_src_sq_obj = SquareModel(cshogi.move_from(self._my_previous_move))
        b_dst_sq_obj = SquareModel(cshogi.move_to(self._my_previous_move))
        a_src_sq_obj = SquareModel(cshogi.move_from(move))
        a_dst_sq_obj = SquareModel(cshogi.move_to(move))

        if (
                a_dst_sq_obj.sq == b_src_sq_obj.sq
            and b_dst_sq_obj.sq == a_src_sq_obj.sq
        ):
            return True

        # それ以外は無視。
        return False
