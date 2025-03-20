import cshogi

from ..logics_o1x.logger_logics import LoggerLogics
from ..models_o2x import Pen


class KomadokuFilterLogics():
    """駒得評価値でフィルタリングします。
    """


    @staticmethod
    def filtering(remaining_moves, gymnasium):

        pen = Pen(table = gymnasium.table)

        if gymnasium.config_doc['debug_mode']['search_do_undo']:
            print('in debug')
            dump_1 = gymnasium.dump()

        best_move_list = []

        pen_best_value = pen.value(-99999)  # 先手なら -99999、後手なら 99999 からスタート。

        # 残った手一覧
        for move in remaining_moves:

            ################
            # MARK: 一手指す
            ################

            # nine_rank_side_value は pen.value() で囲まないこと。
            print(f'before move: {cshogi.move_to_usi(move)} {gymnasium.engine_turn=} {gymnasium.table.turn=} {pen_best_value=} {gymnasium.nine_rank_side_value=}')
            gymnasium.do_move_o1x(move = move)

            # NOTE 一手指した後だから、逆にしてる。
            e1 = pen.swap(gymnasium.nine_rank_side_value, pen_best_value)
            print(f'after move: {cshogi.move_to_usi(move)} {gymnasium.engine_turn=} {gymnasium.table.turn=} {pen_best_value=} {gymnasium.nine_rank_side_value=} {e1[0]=} {e1[1]=} {e1[0] < e1[1]=}')

            if e1[0] < e1[1]:
                pen_best_value = gymnasium.nine_rank_side_value
                best_move_list = [move]
                
            elif pen_best_value == gymnasium.nine_rank_side_value:
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
