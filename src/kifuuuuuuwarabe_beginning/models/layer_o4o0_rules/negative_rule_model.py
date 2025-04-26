from ..layer_o1o0 import constants
from ..layer_o3o0 import RuleModel


class NegativeRuleModel(RuleModel):


    def __init__(self, id, label, basketball_court_model):
        super().__init__(
                id                      = id,
                label                   = label,
                basketball_court_model  = basketball_court_model)


    def after_best_moving_in_idling(self, move, table):
        """（アイドリング中の号令について）指す手の確定時。
        """
        self._after_best_moving_in_idling_nrm(
                move    = move,
                table   = table)


    def on_node_exit_negative(self, remaining_moves, table):
        """ノード来訪時。
        """
        if not self.is_enabled:
            return remaining_moves
        
        # （事前リムーブ分岐）条件が合致したら、このルールをリストから除外する処理。
        if self._remove_rule_on_node_entry_negative(
                remaining_moves = remaining_moves,
                table           = table):
            # （処理を行わず）このオブジェクトを除外
            self._is_removed = True
            return remaining_moves
        
        # （事前スキップ判定）条件に一致したら、スキップする処理。
        if self._skip_step_on_node_entry_negative(
                remaining_moves = remaining_moves,
                table           = table):
             return remaining_moves

        self._on_node_entry_negative(
                remaining_moves = remaining_moves,
                table           = table)

        for i in range(len(remaining_moves))[::-1]:     # `[::-1]` - 逆順
            m = remaining_moves[i]
            mind = self._on_node_exit_negative(m, table)
            if mind == constants.mind.WILL_NOT:
                del remaining_moves[i]

        return remaining_moves


    def after_best_moving_o1o1o0(self, move, table):
        """指す手の確定時。
        """
        self._after_best_moving_negative(
                move    = move,
                table   = table)


    ##########################
    # MARK: バーチャルメソッド
    ##########################

    def _remove_rule_on_node_entry_negative(self, remaining_moves, table):
        """ノード来訪時削除条件。
        真なら、このルールをリストから除外します。
        """
        return False


    def _skip_step_on_node_entry_negative(self, remaining_moves, table):
        """ノード来訪時スキップ条件。
        真なら、ノード来訪時ステップではこのルールをスキップします。
        """
        return False


    def _on_node_entry_negative(self, remaining_moves, table):
        """ノード来訪時。
        """
        pass


    def _on_node_exit_negative(self, move, table):
        """指す前に。
        """
        pass


    def _after_best_moving_in_idling_nrm(self, move, table):
        """（アイドリング中の号令について）指す手の確定時。
        """
        pass


    def _after_best_moving_negative(self, move, table):
        """指す手の確定時。
        """
        pass
