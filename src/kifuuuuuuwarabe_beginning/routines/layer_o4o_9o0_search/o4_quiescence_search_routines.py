import cshogi
import time

from ...models.layer_o1o_9o0 import PieceValuesModel
from ...models.layer_o1o0 import constants, SquareModel
from ...models.layer_o1o0o_9o0_table_helper import TableHelper
from .o5z_quiescence_search_routines import O5zQuiescenceSearchRoutines
from .search_routines import SearchRoutines


INFO_DEPTH = 4


class O4QuiescenceSearchRoutines(SearchRoutines):
    """駒の取り合いのための静止探索。
    駒の取り合いが終わるまで、駒の取り合いを探索します。
    """


    ######################
    # MARK: 縦の辺を伸ばす
    ######################

    @staticmethod
    def extend_vertical_edges_o4(pv_list, search_context_model):
        """縦の辺を伸ばす。
        """

        # PVリスト探索
        # ------------
        for pv in pv_list:

            # 履歴を全部指す前
            # ----------------
            my_move                         = pv.leafer_move_pv
            cap_pt                          = pv.leafer_cap_pt_pv
            piece_exchange_value_on_earth   = pv.leafer_value_pv

            # 履歴を全部指す
            # --------------
            SearchRoutines.do_move_vertical_all(pv=pv, search_context_model=search_context_model)

            # 履歴を全部指した後
            # ------------------
            search_context_model.number_of_visited_nodes += 1
            search_context_model.gymnasium.health_check_qs_model.append_edge_qs(move=my_move, cap_pt=cap_pt, value=piece_exchange_value_on_earth, comment='')

            # 相手番の処理
            # ------------

            # 一手も指さずに局面を見て、終局なら終局外を付加。
            O5zQuiescenceSearchRoutines.set_termination_if_it_o5(parent_pv=pv, search_context_model=search_context_model)

            # 履歴を全部戻す
            # --------------
            SearchRoutines.undo_move_vertical_all(pv=pv, search_context_model=search_context_model)

            # 履歴を全部戻した後
            # ------------------
            search_context_model.gymnasium.health_check_qs_model.pop_node_qs()


    ######################################################
    # MARK: 一手も指さずに局面を見て、終局なら終局外を付加
    ######################################################

    @staticmethod
    def set_termination_if_it_o4(parent_pv, search_context_model):
        """一手も指さずに局面を見て、終局なら終局外を付加。
        手番が回ってきてから、終局が成立するものとする。（何も指さない手番）
        """
        (parent_pv.rooter_backwards_plot_model_pv, parent_pv.is_terminate) = SearchRoutines.look_in_0_moves(
                info_depth              = INFO_DEPTH,
                parent_pv               = parent_pv,
                search_context_model    = search_context_model)


    ################################
    # MARK: 水平指し手をクリーニング
    ################################

    @staticmethod
    def cleaning_horizontal_edges_o4(parent_pv, search_context_model):
        """［水平指し手一覧］をクリーニング。

        Parameters
        ----------
        parent_pv : P rincipalVariationModel
            親手。

        Returns
        -------
        remaining_moves : list<int>
            シーショーギの指し手のリスト。
        """

        legal_move_list = list(search_context_model.gymnasium.table.legal_moves)
        remaining_moves = legal_move_list
        remaining_moves = SearchRoutines.remove_drop_moves(remaining_moves=remaining_moves)           # 打の手を全部除外したい。
        remaining_moves = SearchRoutines.remove_depromoted_moves(remaining_moves=remaining_moves, search_context_model=search_context_model)     # ［成れるのに成らない手］は除外
        (remaining_moves, rolled_back) = SearchRoutines.filtering_same_destination_move_list(parent_move=parent_pv.leafer_move_pv, remaining_moves=remaining_moves, rollback_if_empty=True) # できれば［同］の手を残す。
        remaining_moves = SearchRoutines.get_cheapest_move_list(remaining_moves=remaining_moves)
        (remaining_moves, rolled_back) = SearchRoutines.filtering_capture_or_mate(remaining_moves=remaining_moves, rollback_if_empty=False, search_context_model=search_context_model)       # 駒を取る手と、王手のみ残す
        return remaining_moves


    ################
    # MARK: 手を指す
    ################

    @staticmethod
    def move_all_pv_o4(pv_list, search_context_model):
        """探索の開始。

        Parameters
        ----------
        pv_list : list<P rincipalVariationModel>
            ［読み筋］のリスト。

        Returns
        -------
        pv_list : list<P rincipalVariationModel>
            有力な読み筋。棋譜のようなもの。
            枝が増えて、合法手の数より多くなることがあることに注意。
        """

        # ノード訪問時
        # ------------
        terminated_pv_list = []
        live_pv_list = []

        best_pv             = None  # ベストな子
        best_move           = None
        best_move_cap_pt    = None
        if search_context_model.gymnasium.is_mars:
            best_value = constants.value.BIG_VALUE
        else:
            best_value = constants.value.SMALL_VALUE

        # 各PV
        # ----
        for pv in pv_list:

            ################################
            # MARK: 履歴の最後の一手を指す前
            ################################

            my_move                         = pv.leafer_move_pv
            cap_pt                          = pv.leafer_cap_pt_pv
            piece_exchange_value_on_earth   = pv.leafer_value_pv

            # 履歴を全部指す
            # --------------
            SearchRoutines.do_move_vertical_all(pv=pv, search_context_model=search_context_model)

            # 手番の処理
            # ----------

            # 一手も指さずに局面を見て、終局なら終局外を付加。
            O5zQuiescenceSearchRoutines.set_termination_if_it_o5(parent_pv=pv, search_context_model=search_context_model)

            if pv.is_terminate:                 # 探索不要なら。
                terminated_pv_list.append(pv)   # 終了済みPVリストへ当PVを追加。

            else:
                # ［水平指し手一覧］をクリーニング。
                remaining_moves = O5zQuiescenceSearchRoutines.cleaning_horizontal_edges_o5(parent_pv=pv, search_context_model=search_context_model)

                # ［駒を取る手］がないことを、［静止］と呼ぶ。
                if len(remaining_moves) == 0:
                    pv.rooter_backwards_plot_model_pv = SearchRoutines.create_backwards_plot_model_at_quiescence(info_depth=INFO_DEPTH, search_context_model=search_context_model)
                    pv.is_terminate = True
                    terminated_pv_list.append(pv)

                else:
                    # remaining_moves から pv へ変換。
                    next_pv_list = SearchRoutines.convert_remaining_moves_to_pv_list(parent_pv=pv, remaining_moves=remaining_moves, search_context_model=search_context_model)

                    # # NOTE 再帰は廃止。デバッグ作れないから。
                    # if not pv.is_terminate:
                    #     child_plot_model = O5zQuiescenceSearchRoutines.move_all_pv_o5(
                    #             pv_list     = next_pv_list,
                    #             search_context_model    = search_context_model)
                    # else:
                    #     child_plot_model = pv.rooter_backwards_plot_model_pv

            # MARK: 履歴を全部戻す
            # --------------------
            SearchRoutines.undo_move_vertical_all(pv=pv, search_context_model=search_context_model)

            # MARK: TODO 全ての親手をさかのぼり、［後ろ向き探索の結果］を確定
            # ----------------------------------------------------------

            # # 手番の処理

            # (this_branch_value_on_earth, is_update_best) = SearchRoutines.is_update_best(best_pv=best_pv, child_plot_model=child_plot_model, piece_exchange_value_on_earth=piece_exchange_value_on_earth, search_context_model=search_context_model)
                        
            # # 最善手の更新（１つに絞る）
            # if is_update_best:
            #     best_pv             = pv
            #     best_pv.rooter_backwards_plot_model_pv    = child_plot_model
            #     best_move           = my_move
            #     best_move_cap_pt    = cap_pt
            #     best_value          = this_branch_value_on_earth

        # # 合法手スキャン後

        # # 指したい手がなかったなら、静止探索の末端局面の後ろだ。
        # if best_pv is None:
        #     return SearchRoutines.create_backwards_plot_model_at_no_candidates(info_depth=INFO_DEPTH, search_context_model=search_context_model)

        # # 読み筋に今回の手を付け加える。（ TODO 駒得点も付けたい）
        # best_pv.rooter_backwards_plot_model_pv.append_move_from_back(
        #         move                = best_move,
        #         capture_piece_type  = best_move_cap_pt,
        #         best_value          = best_value,
        #         hint                = '')

        return terminated_pv_list, live_pv_list
