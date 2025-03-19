class Go():


    def __init__(self, gymnasium):
        self._gymnasium = gymnasium


    @staticmethod
    def get_will_play_moves(will_play_moves, gymnasium):

        match_operation_list_to_remove = []

        # 行進リスト
        for march_operation in gymnasium.march_operation_list:
            will_play_moves = march_operation.do_anything(
                    will_play_moves = will_play_moves,
                    table           = gymnasium.table)

            # 行進演算を、必要がなくなったら、リストから除外する操作
            if march_operation.is_removed:
                match_operation_list_to_remove.append(march_operation)

        for march_operation in match_operation_list_to_remove:
            gymnasium.march_operation_list.remove(march_operation)
            print(f'★ get_will_play_moves: 行進演算 削除 {march_operation.label=}')

        return will_play_moves


    @staticmethod
    def on_best_move_played_when_idling(move, gymnasium):
        """（アイドリング中の行進演算について）指す手の確定時。
        """

        match_operation_list_to_activate = []
        match_operation_list_to_remove = []

        # 行進リスト
        for march_operation in gymnasium.march_operation_list_when_idling:
            march_operation.on_best_move_played_when_idling(
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
    def on_best_move_played(move, gymnasium):
        """指す手の確定時。
        """

        match_operation_list_to_remove = []

        # 行進リスト
        for march_operation in gymnasium.march_operation_list:
            march_operation.on_best_move_played(
                    move        = move,
                    table       = gymnasium.table)

            # 行進演算を、必要がなくなったら、リストから除外する操作
            if march_operation.is_removed:
                match_operation_list_to_remove.append(march_operation)

        for march_operation in match_operation_list_to_remove:
            gymnasium.march_operation_list.remove(march_operation)
            print(f'★ ｏn_best_move_played: 行進演算 削除 {march_operation.label=}')
