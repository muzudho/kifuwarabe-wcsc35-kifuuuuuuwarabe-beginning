import cshogi
import time

from ...models.layer_o1o_9o0 import PieceValuesModel
from ...models.layer_o1o0 import constants, SquareModel
from ...models.layer_o1o0o_9o0_table_helper import TableHelper
from .o6_no_search_routines import O6NoSearchRoutines
from .search_routines import SearchRoutines


INFO_DEPTH = 5


class O5zQuiescenceSearchRoutines(SearchRoutines):
    """駒の取り合いのための静止探索。
    駒の取り合いが終わるまで、駒の取り合いを探索します。
    """


    @staticmethod
    def before_search_for_o5(parent_pv, search_context_model):
        (parent_pv.backwards_plot_model, parent_pv.is_terminate) = SearchRoutines.look_in_0_moves(
                info_depth              = INFO_DEPTH,
                parent_pv               = parent_pv,
                search_context_model    = search_context_model)


    @staticmethod
    def search_as_quiescence_o5(pv_list, search_context_model):
        """
        Parameters
        ----------
        parent_move : int
            １手前の手。

        Returns
        -------
        best_prot_model : BackwardsPlotModel
            最善の読み筋。
            これは駒得評価値も算出できる。

        TODO BPMより、最善のPV（PVを延長したもの）を１つ返す方が自然？
        """

        ####################
        # MARK: ノード訪問時
        ####################

        best_pv             = None  # ベストな子
        best_move           = None
        best_move_cap_pt    = None
        if search_context_model.gymnasium.is_mars:
            best_value = constants.value.BIG_VALUE
        else:
            best_value = constants.value.SMALL_VALUE

        for pv in pv_list:

            ################################
            # MARK: 履歴の最後の一手を指す前
            ################################

            my_move                         = pv.last_move_pv
            cap_pt                          = pv.last_cap_pt_pv
            piece_exchange_value_on_earth   = pv.last_value_pv

            ######################
            # MARK: 履歴を全部指す
            ######################

            SearchRoutines.do_move_vertical_all(pv=pv, search_context_model=search_context_model)

            ##########################
            # MARK: 履歴を全部指した後
            ##########################

            search_context_model.number_of_visited_nodes += 1
            search_context_model.gymnasium.health_check_qs_model.append_edge_qs(move=my_move, cap_pt=cap_pt, value=piece_exchange_value_on_earth, comment='')

            ####################
            # MARK: 相手番の処理
            ####################

            O6NoSearchRoutines.before_search_for_o6(parent_pv=pv, search_context_model=search_context_model)

            if pv.is_terminate:
                child_plot_model = pv.backwards_plot_model
            else:
                # NOTE 再帰は廃止。デバッグ作れないから。ここで＜水平線＞。
                child_plot_model = SearchRoutines.create_backwards_plot_model_at_horizon(search_context_model=search_context_model)

            ######################
            # MARK: 履歴を全部戻す
            ######################

            SearchRoutines.undo_move_vertical_all(pv=pv, search_context_model=search_context_model)

            ##########################
            # MARK: 履歴を全部戻した後
            ##########################

            search_context_model.gymnasium.health_check_qs_model.pop_node_qs()

            ##################
            # MARK: 手番の処理
            ##################

            (this_branch_value_on_earth, is_update_best) = SearchRoutines.is_update_best(best_pv=best_pv, child_plot_model=child_plot_model, piece_exchange_value_on_earth=piece_exchange_value_on_earth, search_context_model=search_context_model)
                        
            # 最善手の更新（１つに絞る）
            if is_update_best:
                best_pv                         = pv
                best_pv.backwards_plot_model    = child_plot_model
                best_move                       = my_move
                best_move_cap_pt                = cap_pt
                best_value                      = this_branch_value_on_earth

        ########################
        # MARK: 合法手スキャン後
        ########################

        # 指したい手がなかったなら、静止探索の末端局面の後ろだ。
        if best_pv is None:
            return SearchRoutines.create_backwards_plot_model_at_no_candidates(info_depth=INFO_DEPTH, search_context_model=search_context_model)

        # 読み筋に今回の手を付け加える。（ TODO 駒得点も付けたい）
        best_pv.backwards_plot_model.append_move_from_back(
                move                = best_move,
                capture_piece_type  = best_move_cap_pt,
                best_value          = best_value,
                hint                = '')

        return best_pv.backwards_plot_model
