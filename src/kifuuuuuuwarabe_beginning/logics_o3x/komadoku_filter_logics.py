import cshogi

from ..logics_o1x.logger_logics import LoggerLogics
from ..models_o2x import NineRankSidePerspective


class KomadokuFilterLogics():
    """駒得評価値でフィルタリングします。
    """


    @staticmethod
    def filtering(remaining_moves, gymnasium):

        np = NineRankSidePerspective(
                table = gymnasium.table)
        np_rev = NineRankSidePerspective(
                table           = gymnasium.table,
                after_moving    = True)

        if gymnasium.config_doc['debug_mode']['search_do_undo']:
            print('in debug')
            dump_1 = gymnasium.dump()

        best_move_list = []

        np_best_value = np.value(-99999)  # スタート値。

        # 残った手一覧
        for move in remaining_moves:

            ################
            # MARK: 一手指す
            ################

            # np_value は np.value() で囲まないこと。
            #print(f'before move: {cshogi.move_to_usi(move)} {gymnasium.engine_turn=} {gymnasium.table.turn=} {np_best_value=} {gymnasium.np_value=}')
            gymnasium.do_move_o1x(move = move)

            e1 = np_rev.swap(np_best_value, gymnasium.np_value)
            #print(f'after move: {cshogi.move_to_usi(move)} エンジン手番:{gymnasium.engine_turn} 手番:{gymnasium.table.turn} {np_best_value=} {gymnasium.np_value=} {e1[0]=} {e1[1]=} {e1[0] < e1[1]=}')

            # 更新。
            if e1[0] < e1[1]:
                np_best_value = gymnasium.np_value
                best_move_list = [move]
                
            elif np_best_value == gymnasium.np_value:
                best_move_list.append(move)

            ################
            # MARK: 一手戻す
            ################
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
