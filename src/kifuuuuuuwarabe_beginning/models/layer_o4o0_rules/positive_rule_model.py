from ..layer_o1o0 import constants
from ..layer_o3o0 import RuleModel


class PositiveRuleModel(RuleModel):


    def __init__(self, id, label, basketball_court_model):
        super().__init__(
                id                      = id,
                label                   = label,
                basketball_court_model  = basketball_court_model)


    def after_best_moving_in_idling(self, move, table):
        """（アイドリング中の号令について）指す手の確定時。
        """
        self._after_best_moving_in_idling_prm(
                move    = move,
                table   = table)


    def on_node_entry_positive(self, remaining_moves, table):
        """どの枝も指す前に。

        Returns
        -------
        moves_to_pickup : list<int>
            ピックアップした指し手。
        """

        if not self.is_enabled:
            return []
        
        # （事前リムーブ分岐）条件が合致したら、このルールをリストから除外する処理。
        if self._remove_rule_on_node_entry_positive(
                remaining_moves = remaining_moves,
                table           = table):
            # （処理を行わず）このオブジェクトを除外
            self._is_removed = True
            return []
        
        # （事前スキップ判定）条件に一致したら、スキップする処理。
        if self._skip_step_on_node_entry_positive(
                remaining_moves = remaining_moves,
                table           = table):
             return []

        self._on_node_entry_positive(
                remaining_moves = remaining_moves,
                table           = table)

        moves_to_pickup = []

        for i in range(len(remaining_moves))[::-1]:     # `[::-1]` - 逆順
            m = remaining_moves[i]
            if self._on_node_exit_positive(m, table):
                moves_to_pickup.append(m)

        return moves_to_pickup


    def after_best_moving_o1o1o0(self, move, table):
        """指す手の確定時。
        """
        self._after_best_moving_prm(
                move    = move,
                table   = table)


    ##########################
    # MARK: バーチャルメソッド
    ##########################

    def _remove_rule_on_node_entry_positive(self, remaining_moves, table):
        """ノード来訪時削除条件。
        真なら、このルールをリストから除外します。
        """
        return False


    def _skip_step_on_node_entry_positive(self, remaining_moves, table):
        """ノード来訪時スキップ条件。
        真なら、ノード来訪時ステップではこのルールをスキップします。
        """
        return False


    def _on_node_entry_positive(self, remaining_moves, table):
        """ノード来訪時。

        Returns
        -------
        is_better_move : bool
            指させたい手なら真。
        """


    def _on_node_exit_positive(self, move, table):
        """指す前にこの手に決める。

        Returns
        -------
        is_better_move : bool
            指させたい手なら真。
        """
        pass


    def _after_best_moving_in_idling_prm(self, move, table):
        """（アイドリング中の号令について）指す手の確定時。
        """
        pass


    def _after_best_moving_prm(self, move, table):
        """指す手の確定時。
        """
        pass
