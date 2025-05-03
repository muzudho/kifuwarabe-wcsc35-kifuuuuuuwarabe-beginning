import cshogi
import time

from ...models.layer_o1o0 import SquareModel
from .search_routines import SearchRoutines
from .o2_counter_search_routines import O2CounterSearchRoutines


INFO_DEPTH = 0


class O0NoSearchRoutines(SearchRoutines):
    """０階について無探索。
    """

    ######################
    # MARK: 縦の辺を伸ばす
    ######################

    @staticmethod
    def extend_vertical_edges_o0(pv_list, search_context_model):
        """縦の辺を伸ばす。
        """

        # PVリスト探索
        # ------------
        for pv in pv_list:

            # 相手番の処理
            # ------------

            # 一手も指さずに局面を見て、終局なら終局外を付加。
            O0NoSearchRoutines.set_termination_if_it_o0(parent_pv=pv, search_context_model=search_context_model)


    ######################################################
    # MARK: 一手も指さずに局面を見て、終局なら終局外を付加
    ######################################################

    @staticmethod
    def set_termination_if_it_o0(parent_pv, search_context_model):
        """一手も指さずに局面を見て、終局なら終局外を付加。
        手番が回ってきてから、終局が成立するものとする。（何も指さない手番）
        """
        (parent_pv.rooter_backwards_plot_model_pv, parent_pv.is_terminate) = SearchRoutines.look_in_0_moves(
            info_depth              = INFO_DEPTH,
            parent_pv               = parent_pv,
            search_context_model    = search_context_model)
