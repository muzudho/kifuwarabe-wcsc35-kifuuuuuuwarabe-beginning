import cshogi
import time

from ...models.layer_o1o0 import SquareModel
from .search_routines import SearchRoutines
from .o2_counter_search_routines import O2CounterSearchRoutines


INFO_DEPTH = 0


class O0NoSearchRoutines(SearchRoutines):
    """０階について無探索。
    """

    @staticmethod
    def before_search_for_o0(parent_pv, search_context_model):
        (parent_pv.backwards_plot_model, parent_pv.is_terminate) = SearchRoutines.look_in_0_moves(
            info_depth              = INFO_DEPTH,
            parent_pv               = parent_pv,
            search_context_model    = search_context_model)
