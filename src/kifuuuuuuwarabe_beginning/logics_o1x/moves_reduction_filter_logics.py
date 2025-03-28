class MovesReductionFilterLogics():
    """［合法手削減濾］
    合法手を減らすフィルターです。
    """


    @staticmethod
    def before_move_o1x(remaining_moves, gymnasium):
        """［指前］
        １手指す前です。

        Parameters
        ----------
        remaining_moves : list<usi>
            制約：
                指し手は必ず１つ以上残っています。
        
        Returns
        -------
        remaining_moves : list<usi>
            制約：
                指し手は必ず１つ以上残っています。
                FIXME これで合ってるか要確認。
        """

        old_remaining_moves = remaining_moves.copy()

        negative_rules_to_remove = []

        # 行進リスト
        for negative_rule in gymnasium.negative_rule_collection_model.list_of_active:
            # １手も指さず、目の前にある盤に対して。
            remaining_moves = negative_rule.before_move_o1o1x(
                    remaining_moves = remaining_moves,
                    table           = gymnasium.table)

            # 行進演算を、必要がなくなったら、リストから除外する操作
            if negative_rule.is_removed:
                negative_rules_to_remove.append(negative_rule)

        for negative_rule in negative_rules_to_remove:
            gymnasium.negative_rule_collection_model.list_of_active.remove(negative_rule)
            gymnasium.thinking_logger_module.append(f"[moves_reduction_filter_logics.py > before_move_o1x] delete negative rule. {negative_rule.label}")
        # 指し手が全部消えてしまった場合、何でも指すようにします
        if len(remaining_moves) < 1:
            return old_remaining_moves

        return remaining_moves


    @staticmethod
    def after_best_moving(move, gymnasium):
        """［指後］
        １手指した後に呼び出されます。
        指す手の確定時。
        """


        def _for_idle_negative_rules(move, gymnasium):
            """［指後、待機者用］
            １手指した後に呼び出されます。
            （アイドリング中の行進演算について）指す手の確定時。
            """

            negative_rules_to_activate = []
            negative_rules_to_remove = []

            # 行進リスト
            for negative_rule in gymnasium.negative_rule_collection_model.list_of_idle:
                negative_rule.after_best_moving_in_idling(
                        move        = move,
                        table       = gymnasium.table)

                if negative_rule.is_activate:
                    negative_rules_to_activate.append(negative_rule)

                # 行進演算を、必要がなくなったら、リストから除外する操作
                if negative_rule.is_removed:
                    negative_rules_to_remove.append(negative_rule)

            for negative_rule in negative_rules_to_activate:
                gymnasium.negative_rule_collection_model.list_of_idle.remove(negative_rule)
                gymnasium.negative_rule_collection_model.list_of_active.append(negative_rule)
                gymnasium.thinking_logger_module.append(f"[moves_reduction_filter_logics.py > after_best_moving] activate negative rule. {negative_rule.label}")

            for negative_rule in negative_rules_to_remove:
                gymnasium.negative_rule_collection_model.list_of_active.remove(negative_rule)
                gymnasium.thinking_logger_module.append(f"[moves_reduction_filter_logics.py > after_best_moving] delete negative rule. {negative_rule.label}")


        _for_idle_negative_rules(
                move        = move,
                gymnasium   = gymnasium)

        negative_rules_to_remove = []

        # 行進リスト
        for negative_rule in gymnasium.negative_rule_collection_model.list_of_active:
            negative_rule.after_best_moving(
                    move        = move,
                    table       = gymnasium.table)

            # 行進演算を、必要がなくなったら、リストから除外する操作
            if negative_rule.is_removed:
                negative_rules_to_remove.append(negative_rule)

        for negative_rule in negative_rules_to_remove:
            gymnasium.negative_rule_collection_model.list_of_active.remove(negative_rule)
            gymnasium.thinking_logger_module.append(f"[moves_reduction_filter_logics.py > after_best_moving] delete negative rule. {negative_rule.label}")
