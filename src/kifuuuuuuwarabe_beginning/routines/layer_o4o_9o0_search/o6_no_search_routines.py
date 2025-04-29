import cshogi
import time

from ...models.layer_o1o_9o0 import PieceValuesModel
from ...models.layer_o1o0 import constants, SquareModel
from ...models.layer_o1o0o_9o0_table_helper import TableHelper
from .search_routines import SearchRoutines


INFO_DEPTH = 6


class O6NoSearchRoutines(SearchRoutines):


    @staticmethod
    def before_search_for_o6(parent_pv, search_context_model):
        (parent_pv.backwards_plot_model, parent_pv.is_terminate) = SearchRoutines.look_in_0_moves(
                info_depth              = INFO_DEPTH,
                parent_pv               = parent_pv,
                search_context_model    = search_context_model)
