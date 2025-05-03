import cshogi
import time

from ...models.layer_o1o0 import constants, SquareModel
from .search_routines import SearchRoutines
from .o3_quiescence_search_routines import O3QuiescenceSearchRoutines


INFO_DEPTH = 2


class O2CounterSearchRoutines(SearchRoutines):
    """２階の探索。
    """

    ######################
    # MARK: 縦の辺を伸ばす
    ######################

    @staticmethod
    def extend_vertical_edges_o2(pv_list, search_context_model):
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
            search_context_model.number_of_visited_nodes  += 1
            search_context_model.gymnasium.health_check_qs_model.append_edge_qs(move=my_move, cap_pt=cap_pt, value=piece_exchange_value_on_earth, comment='')

            # 相手番の処理
            # ------------

            # 一手も指さずに局面を見て、終局なら終局外を付加。
            O2CounterSearchRoutines.set_termination_if_it_o2(parent_pv=pv, search_context_model=search_context_model)

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
    def set_termination_if_it_o2(parent_pv, search_context_model):
        """一手も指さずに局面を見て、終局なら終局外を付加。
        手番が回ってきてから、終局が成立するものとする。（何も指さない手番）
        """
        (parent_pv.deprecated_rooter_backwards_plot_model_pv, parent_pv.is_terminate) = SearchRoutines.look_in_0_moves(
                info_depth              = INFO_DEPTH,
                parent_pv               = parent_pv,
                search_context_model    = search_context_model)


    ################################
    # MARK: 水平指し手をクリーニング
    ################################

    @staticmethod
    def cleaning_horizontal_edges_o2(parent_pv, search_context_model):
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
        
        remaining_moves = list(search_context_model.gymnasium.table.legal_moves)      # 全合法手。
        remaining_moves = SearchRoutines.remove_depromoted_moves(remaining_moves=remaining_moves, search_context_model=search_context_model)     # ［成れるのに成らない手］は除外
        aigoma_move_list = O2CounterSearchRoutines._choice_aigoma_move_list(remaining_moves=remaining_moves, search_context_model=search_context_model)   # ［間駒］（相手の利きの上に置く手）を抽出。
        remaining_moves = O2CounterSearchRoutines._remove_drop_except_aigoma(remaining_moves)  # ［間駒］以外の［打］は（多すぎるので）除外。
        (remaining_moves, rolled_back) = SearchRoutines.filtering_capture_or_mate(remaining_moves=remaining_moves, rollback_if_empty=True, search_context_model=search_context_model)    # ［カウンター探索］では、駒を取る手と、王手のみ残す。［駒を取る手、王手］が無ければ、（巻き戻して）それ以外の手を指します。
        remaining_moves.extend(aigoma_move_list)
        return remaining_moves


    ################
    # MARK: 手を指す
    ################

    @staticmethod
    def move_all_pv_o2(pv_list, search_context_model):
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

        # 各PV
        # ----
        for pv in pv_list:

            # 履歴を全部指す
            # --------------
            SearchRoutines.do_move_vertical_all(pv=pv, search_context_model=search_context_model)

            # 手番の処理
            # ----------

            if pv.is_terminate:                 # 探索不要なら。
                terminated_pv_list.append(pv)   # 終了済みPVリストへ当PVを追加。

            else:
                # ［水平指し手一覧］をクリーニング。
                remaining_moves = O3QuiescenceSearchRoutines.cleaning_horizontal_edges_o3(parent_pv=pv, search_context_model=search_context_model)

                # ［駒を取る手］がないことを、［静止］と呼ぶ。
                if len(remaining_moves) == 0:
                    pv.set_deprecated_rooter_backwards_plot_model_pv(SearchRoutines.create_backwards_plot_model_at_quiescence(info_depth=INFO_DEPTH, search_context_model=search_context_model))
                    pv.is_terminate = True
                    terminated_pv_list.append(pv)

                else:
                    # remaining_moves から pv へ変換。
                    next_pv_list = SearchRoutines.convert_remaining_moves_to_pv_list(parent_pv=pv, remaining_moves=remaining_moves, search_context_model=search_context_model)

                    # # TODO ３手目を指す。
                    # next_pv.set_deprecated_rooter_backwards_plot_model_pv(O3QuiescenceSearchRoutines.move_all_pv_o3(
                    #         pv_list                 = next_pv_list,
                    #         search_context_model    = search_context_model))

                    # for next_pv in reversed(next_pv_list):          # 各［次PV］。
                    #     if next_pv.is_terminate:                    # 次の読み筋が終了していれば。
                    #         terminated_pv_list.append(next_pv)      # 終了済みPVリストへ［次PV］を追加。
                    #     else:
                    #         live_pv_list.append(next_pv)            # 残PVリストへ［次PV］を追加。

            # MARK: 履歴を全部戻す
            # --------------------
            SearchRoutines.undo_move_vertical_all(pv=pv, search_context_model=search_context_model)

            # MARK: TODO 全ての親手をさかのぼり、［後ろ向き探索の結果］を確定
            # ----------------------------------------------------------

            # １階の手は、全ての手の読み筋を記憶します。最善手は選びません。
            pv.deprecated_rooter_backwards_plot_model_pv.append_move_from_back(
                    move                = pv.leafer_move_pv,
                    capture_piece_type  = pv.leafer_cap_pt_pv,
                    best_value          = pv.deprecated_rooter_backwards_plot_model_pv.get_exchange_value_on_earth(),
                    hint                = '')

            #(this_branch_value_on_earth, is_update_best) = SearchRoutines.is_update_best(best_pv=best_pv, child_plot_model=child_plot_model, piece_exchange_value_on_earth=piece_exchange_value_on_earth, search_context_model=search_context_model)

            # # 最善手の更新
            # if is_update_best:
            #     best_pv             = pv
            #     best_pv.set_deprecated_rooter_backwards_plot_model_pv(child_plot_model)
            #     best_move           = my_move
            #     best_move_cap_pt    = cap_pt
            #     best_value          = this_branch_value_on_earth

            # ベータカットもしません。全部返すから。

        ######################
        # MARK: PVリスト探索後
        ######################

        # # 指したい手がなかったなら、静止探索の末端局面の後ろだ。
        # if best_pv is None:
        #     return SearchRoutines.create_backwards_plot_model_at_no_candidates(info_depth=INFO_DEPTH, search_context_model=search_context_model)

        # # 今回の手を付け加える。
        # best_pv.deprecated_rooter_backwards_plot_model_pv.append_move_from_back(
        #         move                = best_move,
        #         capture_piece_type  = best_move_cap_pt,
        #         best_value          = best_value,
        #         hint                = '')

        return terminated_pv_list, live_pv_list


    ####################
    # MARK: サブルーチン
    ####################

    @staticmethod
    def _choice_aigoma_move_list(remaining_moves, search_context_model):
        # TODO ［間駒］（相手の利きの上に置く手）を抽出。
        aigoma_move_list = []
        for my_move in remaining_moves:
            dst_sq_obj  = SquareModel(cshogi.move_to(my_move))      # ［移動先マス］
            is_aigoma = search_context_model.get_root_searched_control_map(sq=dst_sq_obj.sq)
            if is_aigoma:
                aigoma_move_list.append(my_move)
        return aigoma_move_list


    @staticmethod
    def _remove_drop_except_aigoma(remaining_moves):
        # ［間駒］以外の［打］は（多すぎるので）除外。
        for my_move in reversed(remaining_moves):
            is_drop = cshogi.move_is_drop(my_move)
            if is_drop:
                remaining_moves.remove(my_move)
        return remaining_moves
