class MovesPickupFilterLogics():
    """［合法手ピックアップ］
    合法手のリストから１つを選ぶフィルターです。
    """


    @staticmethod
    def before_branches_o1x(remaining_moves, gymnasium):
        """［指前］
        どの手も指す前です。

        Parameters
        ----------
        remaining_moves : list<usi>
            制約：
                指し手は必ず１つ以上残っています。
        
        Returns
        -------
        moves_to_pickup : list<usi>
            ピックアップした手のリスト。
        """

        moves_to_pickup = []
        positive_rules_to_remove = []

        # 号令リスト
        for positive_rule in gymnasium.gourei_collection_model.positive_rule_list_of_active:
            # １手も指さず、目の前にある盤に対して。
            temp_moves_to_pickup = positive_rule.before_branches_o1o1x(
                    remaining_moves = remaining_moves,
                    table           = gymnasium.table)
            moves_to_pickup.extend(temp_moves_to_pickup)

            # 号令を、必要がなくなったら、リストから除外する操作
            if positive_rule.is_removed:
                positive_rules_to_remove.append(positive_rule)

        for positive_rule in positive_rules_to_remove:
            gymnasium.gourei_collection_model.positive_rule_list_of_active.remove(positive_rule)
            gymnasium.thinking_logger_module.append(f"[moves_pickup_filter_logics.py > before_branches_o1x] delete positive rule. {positive_rule.label}")

        return moves_to_pickup
