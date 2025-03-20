class MovesReductionFilterLogics():
    """［合法手削減濾］
    合法手を減らすフィルターです。
    """


    @staticmethod
    def before_move_o1(remaining_moves, gymnasium):
        """［指前］
        １手指す前です。
        """

        negative_rules_to_remove = []

        # 行進リスト
        for negative_rule in gymnasium.list_of_negative_rules:
            # １手も指さず、目の前にある盤に対して。
            remaining_moves = negative_rule.before_move_o1o1(
                    remaining_moves = remaining_moves,
                    table           = gymnasium.table)

            # 行進演算を、必要がなくなったら、リストから除外する操作
            if negative_rule.is_removed:
                negative_rules_to_remove.append(negative_rule)

        for negative_rule in negative_rules_to_remove:
            gymnasium.list_of_negative_rules.remove(negative_rule)
            print(f'★ before_move_o1: 行進演算 削除 {negative_rule.label=}')

        return remaining_moves


    @staticmethod
    def after_best_moving_when_idling(move, gymnasium):
        """［指後、待機者用］
        １手指した後に呼び出されます。
        （アイドリング中の行進演算について）指す手の確定時。
        """

        negative_rules_to_activate = []
        negative_rules_to_remove = []

        # 行進リスト
        for negative_rule in gymnasium.list_of_idle_negative_rules:
            negative_rule.after_best_moving_when_idling(
                    move        = move,
                    table       = gymnasium.table)

            if negative_rule.is_activate:
                negative_rules_to_activate.append(negative_rule)

            # 行進演算を、必要がなくなったら、リストから除外する操作
            if negative_rule.is_removed:
                negative_rules_to_remove.append(negative_rule)

        for negative_rule in negative_rules_to_activate:
            gymnasium.list_of_idle_negative_rules.remove(negative_rule)
            gymnasium.list_of_negative_rules.append(negative_rule)
            print(f'★ ｏn_best_move_played: 行進演算 有効化 {negative_rule.label=}')

        for negative_rule in negative_rules_to_remove:
            gymnasium.list_of_negative_rules.remove(negative_rule)
            print(f'★ ｏn_best_move_played: 行進演算 削除 {negative_rule.label=}')


    @staticmethod
    def after_best_moving(move, gymnasium):
        """［指後］
        １手指した後に呼び出されます。
        指す手の確定時。
        """

        negative_rules_to_remove = []

        # 行進リスト
        for negative_rule in gymnasium.list_of_negative_rules:
            negative_rule.after_best_moving(
                    move        = move,
                    table       = gymnasium.table)

            # 行進演算を、必要がなくなったら、リストから除外する操作
            if negative_rule.is_removed:
                negative_rules_to_remove.append(negative_rule)

        for negative_rule in negative_rules_to_remove:
            gymnasium.list_of_negative_rules.remove(negative_rule)
            print(f'★ ｏn_best_move_played: 行進演算 削除 {negative_rule.label=}')
