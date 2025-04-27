import cshogi

from ...routines.layer_o1o0.logger_routines import LoggerRoutines
from ..layer_o2o0 import NineRankSidePerspectiveModel


class KomadokuFilterModel():
    """駒得評価値でフィルタリングします。
    """


    def __init__(self, gymnasium):
        self._gymnasium             = gymnasium
        self._old_remaining_moves   = None
        self._np                    = None
        self._np_rev                = None
        self._dump_1                = None
        self._best_move_list        = None
        self._np_best_value         = None


    def before_loop(self, remaining_moves):
        self._old_remaining_moves = remaining_moves.copy()
        self._np = NineRankSidePerspectiveModel(
                table = self._gymnasium.table)
        self._np_rev = NineRankSidePerspectiveModel(
                table           = self._gymnasium.table,
                after_moving    = True)

        if self._gymnasium.config_doc['debug_mode']['search_do_undo']:
            print('in debug')
            self._dump_1 = self._gymnasium.dump()

        self._best_move_list = []
        self._np_best_value = self._np.value(-99999)  # スタート値。


    def after_moving(self, move):
        """１手指した後
        """
        (a, b) = self._np_rev.swap(self._np_best_value, self._gymnasium.np_value)
        #print(f'after move: {cshogi.move_to_usi(move)} エンジン手番:{gymnasium.earth_turn} 手番:{gymnasium.table.turn} {np_best_value=} {gymnasium.np_value=} {a=} {b=} {a < b=}')

        # 更新。
        if a < b:
            self._np_best_value = self._gymnasium.np_value
            self._best_move_list = [move]
            
        elif self._np_best_value == self._gymnasium.np_value:
            self._best_move_list.append(move)


    def after_undo_moving(self, removed_move):
        if self._gymnasium.config_doc['debug_mode']['search_do_undo']:
            dump_2 = self._gymnasium.dump()
            if self._dump_1 != dump_2:

                LoggerRoutines.DumpDiffError(
                        dump_1  = self._dump_1,
                        dump_2  = dump_2)

                raise ValueError(f"dump error in search")


    def after_loop(self):
        # 指し手が全部消えてしまった場合、何でも指すようにします
        if len(self._best_move_list) < 1:
            return self._old_remaining_moves
        
        return self._best_move_list
