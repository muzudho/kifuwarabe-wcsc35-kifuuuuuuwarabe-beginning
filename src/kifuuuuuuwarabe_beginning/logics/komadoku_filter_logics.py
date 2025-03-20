from .logger_logics import LoggerLogics


class KomadokuFilterLogics():
    """駒得評価値でフィルタリングします。
    """


    @staticmethod
    def filtering(remaining_moves, gymnasium):

        if gymnasium.config_doc['debug_mode']['search_do_undo']:
            print('in debug')
            dump_1 = gymnasium.dump()

        best_move_list = []
        #best_value = 
        max_engine_value = -99999   # 無さそうな最低値。

        # 残った手一覧
        for move in remaining_moves:

            # 一手指す
            gymnasium.do_move_o1x(move = move)
            #print(f'move: {cshogi.move_to_usi(move)} {gymnasium.nine_rank_side_value=} {gymnasium.engine_turn=} {gymnasium.engine_value=}')

            if max_engine_value < gymnasium.engine_value:
                max_engine_value = gymnasium.engine_value
                best_move_list = [move]
            elif max_engine_value == gymnasium.engine_value:
                best_move_list.append(move)

            # 一手戻す
            gymnasium.undo_move_o1x()

            if gymnasium.config_doc['debug_mode']['search_do_undo']:
                dump_2 = gymnasium.dump()
                if dump_1 != dump_2:

                    LoggerLogics.DumpDiffError(
                            dump_1  = dump_1,
                            dump_2  = dump_2)

                    raise ValueError(f"dump error in search")

        # 指し手が全部消えてしまった場合、何でも指すようにします
        if len(best_move_list) < 1:
            return remaining_moves

        return best_move_list
