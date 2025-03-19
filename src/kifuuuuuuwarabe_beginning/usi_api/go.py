class Go():


    def __init__(self, gymnasium, config_doc):
        self._gymnasium = gymnasium


    def get_will_play_moves(self, will_play_moves, table, config_doc):

        match_operation_list_to_remove = []

        # 行進リスト
        for march_operation in self._gymnasium.march_operation_list:
            will_play_moves = march_operation.do_anything(
                    will_play_moves = will_play_moves,
                    table           = table)

            # 行進演算を、必要がなくなったら、リストから除外する操作
            if march_operation.is_removed:
                match_operation_list_to_remove.append(march_operation)

        for march_operation in match_operation_list_to_remove:
            self._gymnasium.march_operation_list.remove(march_operation)
            print(f'★ get_will_play_moves: 行進演算 削除 {march_operation.label=}')

        return will_play_moves


    def on_best_move_played_when_idling(self, move, table):
        """（アイドリング中の行進演算について）指す手の確定時。
        """

        match_operation_list_to_activate = []
        match_operation_list_to_remove = []

        # 行進リスト
        for march_operation in self._gymnasium.march_operation_list_when_idling:
            march_operation.on_best_move_played_when_idling(
                    move        = move,
                    table       = table)

            if march_operation.is_activate:
                match_operation_list_to_activate.append(march_operation)

            # 行進演算を、必要がなくなったら、リストから除外する操作
            if march_operation.is_removed:
                match_operation_list_to_remove.append(march_operation)

        for march_operation in match_operation_list_to_activate:
            self._gymnasium.march_operation_list_when_idling.remove(march_operation)
            self._gymnasium.march_operation_list.append(march_operation)
            print(f'★ ｏn_best_move_played: 行進演算 有効化 {march_operation.label=}')

        for march_operation in match_operation_list_to_remove:
            self._gymnasium.march_operation_list.remove(march_operation)
            print(f'★ ｏn_best_move_played: 行進演算 削除 {march_operation.label=}')


    def on_best_move_played(self, move, table):
        """指す手の確定時。
        """

        match_operation_list_to_remove = []

        # 行進リスト
        for march_operation in self._gymnasium.march_operation_list:
            march_operation.on_best_move_played(
                    move        = move,
                    table       = table)

            # 行進演算を、必要がなくなったら、リストから除外する操作
            if march_operation.is_removed:
                match_operation_list_to_remove.append(march_operation)

        for march_operation in match_operation_list_to_remove:
            self._gymnasium.march_operation_list.remove(march_operation)
            print(f'★ ｏn_best_move_played: 行進演算 削除 {march_operation.label=}')
