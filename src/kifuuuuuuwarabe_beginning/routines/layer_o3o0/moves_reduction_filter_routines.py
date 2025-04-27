class MovesReductionFilterRoutines():
    """［合法手削減濾］
    合法手を減らすフィルターです。
    """


    @staticmethod
    def on_node_entry_negative(remaining_moves, gymnasium):
        """［指前］
        どの手も指す前です。

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

        negative_rules_to_remove = []

        # 号令リスト
        for negative_rule in gymnasium.gourei_collection_model.negative_rule_list_of_active:
            old_remaining_moves = remaining_moves.copy()    # バックアップ

            # １手も指さず、目の前にある盤に対して。
            remaining_moves = negative_rule.on_node_exit_negative(
                    remaining_moves = remaining_moves,
                    table           = gymnasium.table)

            # 号令を、必要がなくなったら、リストから除外する操作
            if negative_rule.is_removed:
                negative_rules_to_remove.append(negative_rule)

            # 指し手が全部消えてしまった場合、この操作をアンドゥします。
            if len(remaining_moves) < 1:
                remaining_moves = old_remaining_moves

            # ログ貯蓄
            for move in remaining_moves:
                gymnasium.health_check_go_model.append_health(
                        move    = move,
                        name    = f"NR[{negative_rule.id}]",
                        value   = True)

        for negative_rule in negative_rules_to_remove:
            gymnasium.gourei_collection_model.negative_rule_list_of_active.remove(negative_rule)
            gymnasium.thinking_logger_module.append_message(f"[moves_reduction_filter_logics.py > on_node_entry_negative] delete negative rule. {negative_rule.label}")


        return remaining_moves


    @staticmethod
    def after_best_moving_o1o0(move, gymnasium):
        """［指後］
        １手指した後に呼び出されます。
        指す手の確定時。
        """


        def _for_idle_negative_rules(move, gymnasium):
            """［指後、待機者用］
            １手指した後に呼び出されます。
            （アイドリング中の号令について）指す手の確定時。
            """

            negative_rules_to_activate = []
            negative_rules_to_remove = []

            # 号令リスト
            for negative_rule in gymnasium.gourei_collection_model.negative_rule_list_of_idle:
                negative_rule.after_best_moving_in_idling(
                        move        = move,
                        table       = gymnasium.table)

                if negative_rule.is_activate:
                    negative_rules_to_activate.append(negative_rule)

                # 号令を、必要がなくなったら、リストから除外する操作
                if negative_rule.is_removed:
                    negative_rules_to_remove.append(negative_rule)

            for negative_rule in negative_rules_to_activate:
                gymnasium.gourei_collection_model.negative_rule_list_of_idle.remove(negative_rule)
                gymnasium.gourei_collection_model.negative_rule_list_of_active.append(negative_rule)
                gymnasium.thinking_logger_module.append_message(f"[moves_reduction_filter_logics.py > after_best_moving_o1o0] activate negative rule. {negative_rule.label}")

            for negative_rule in negative_rules_to_remove:
                gymnasium.gourei_collection_model.negative_rule_list_of_active.remove(negative_rule)
                gymnasium.thinking_logger_module.append_message(f"[moves_reduction_filter_logics.py > after_best_moving_o1o0] delete negative rule. {negative_rule.label}")


        _for_idle_negative_rules(
                move        = move,
                gymnasium   = gymnasium)

        negative_rules_to_remove = []

        # 号令リスト
        for negative_rule in gymnasium.gourei_collection_model.negative_rule_list_of_active:
            negative_rule.after_best_moving_o1o1o0(
                    move        = move,
                    table       = gymnasium.table)

            # 号令を、必要がなくなったら、リストから除外する操作
            if negative_rule.is_removed:
                negative_rules_to_remove.append(negative_rule)

        for negative_rule in negative_rules_to_remove:
            gymnasium.gourei_collection_model.negative_rule_list_of_active.remove(negative_rule)
            gymnasium.thinking_logger_module.append_message(f"[moves_reduction_filter_logics.py > after_best_moving_o1o0] delete negative rule. {negative_rule.label}")
