class GoLogics():


    @staticmethod
    def before_move_o1(will_play_moves, gymnasium):
        """主処理。
        """

        match_operation_list_to_remove = []

        # 行進リスト
        for march_operation in gymnasium.march_operation_list:
            # １手も指さず、目の前にある盤に対して。
            will_play_moves = march_operation.before_move_o1o1(
                    will_play_moves = will_play_moves,
                    table           = gymnasium.table)

            # 行進演算を、必要がなくなったら、リストから除外する操作
            if march_operation.is_removed:
                match_operation_list_to_remove.append(march_operation)

        for march_operation in match_operation_list_to_remove:
            gymnasium.march_operation_list.remove(march_operation)
            print(f'★ before_move_o1: 行進演算 削除 {march_operation.label=}')

        return will_play_moves


    @staticmethod
    def after_best_moving_when_idling(move, gymnasium):
        """１手指した後に呼び出されます。
        （アイドリング中の行進演算について）指す手の確定時。
        """

        match_operation_list_to_activate = []
        match_operation_list_to_remove = []

        # 行進リスト
        for march_operation in gymnasium.march_operation_list_when_idling:
            march_operation.after_best_moving_when_idling(
                    move        = move,
                    table       = gymnasium.table)

            if march_operation.is_activate:
                match_operation_list_to_activate.append(march_operation)

            # 行進演算を、必要がなくなったら、リストから除外する操作
            if march_operation.is_removed:
                match_operation_list_to_remove.append(march_operation)

        for march_operation in match_operation_list_to_activate:
            gymnasium.march_operation_list_when_idling.remove(march_operation)
            gymnasium.march_operation_list.append(march_operation)
            print(f'★ ｏn_best_move_played: 行進演算 有効化 {march_operation.label=}')

        for march_operation in match_operation_list_to_remove:
            gymnasium.march_operation_list.remove(march_operation)
            print(f'★ ｏn_best_move_played: 行進演算 削除 {march_operation.label=}')


    @staticmethod
    def after_best_moving(move, gymnasium):
        """１手指した後に呼び出されます。
        指す手の確定時。
        """

        match_operation_list_to_remove = []

        # 行進リスト
        for march_operation in gymnasium.march_operation_list:
            march_operation.after_best_moving(
                    move        = move,
                    table       = gymnasium.table)

            # 行進演算を、必要がなくなったら、リストから除外する操作
            if march_operation.is_removed:
                match_operation_list_to_remove.append(march_operation)

        for march_operation in match_operation_list_to_remove:
            gymnasium.march_operation_list.remove(march_operation)
            print(f'★ ｏn_best_move_played: 行進演算 削除 {march_operation.label=}')
