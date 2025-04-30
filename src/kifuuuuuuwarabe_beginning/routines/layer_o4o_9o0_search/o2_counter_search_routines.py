import cshogi
import time

from ...models.layer_o1o0 import constants, SquareModel
from .search_routines import SearchRoutines
from .o3_quiescence_search_routines import O3QuiescenceSearchRoutines


INFO_DEPTH = 2


class O2CounterSearchRoutines(SearchRoutines):
    """２階の探索。
    """


    @staticmethod
    def cleaning_horizontal_edges_o2(parent_pv, search_context_model):
        """水平指し手一覧］をクリーニング。

        Parameters
        ----------
        parent_pv : PrincipalVariationModel
            親手。

        Returns
        -------
        remaining_moves : list<int>
            デバッグの都合。シーショーギの指し手のリスト。
        """
        
        remaining_moves = list(search_context_model.gymnasium.table.legal_moves)      # 全合法手。
        remaining_moves = SearchRoutines.remove_depromoted_moves(remaining_moves=remaining_moves, search_context_model=search_context_model)     # ［成れるのに成らない手］は除外
        aigoma_move_list = O2CounterSearchRoutines._choice_aigoma_move_list(remaining_moves=remaining_moves, search_context_model=search_context_model)   # ［間駒］（相手の利きの上に置く手）を抽出。
        remaining_moves = O2CounterSearchRoutines._remove_drop_except_aigoma(remaining_moves)  # ［間駒］以外の［打］は（多すぎるので）除外。
        (remaining_moves, rolled_back) = SearchRoutines.filtering_capture_or_mate(remaining_moves=remaining_moves, rollback_if_empty=True, search_context_model=search_context_model)    # ［カウンター探索］では、駒を取る手と、王手のみ残す。［駒を取る手、王手］が無ければ、（巻き戻して）それ以外の手を指します。
        remaining_moves.extend(aigoma_move_list)

        return remaining_moves


    @staticmethod
    def extend_vertical_edges_o2(pv_list, search_context_model):
        """縦の辺を伸ばす。
        """

        ####################
        # MARK: PVリスト探索
        ####################

        for pv in pv_list:

            ########################
            # MARK: 履歴を全部指す前
            ########################

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

            search_context_model.number_of_visited_nodes  += 1
            search_context_model.gymnasium.health_check_qs_model.append_edge_qs(move=my_move, cap_pt=cap_pt, value=piece_exchange_value_on_earth, comment='')

            ####################
            # MARK: 相手番の処理
            ####################

            # PV を更新。
            O2CounterSearchRoutines.before_search_for_o2(parent_pv=pv, search_context_model=search_context_model)
                        
            ######################
            # MARK: 履歴を全部戻す
            ######################

            SearchRoutines.undo_move_vertical_all(pv=pv, search_context_model=search_context_model)

            ##########################
            # MARK: 履歴を全部戻した後
            ##########################

            search_context_model.gymnasium.health_check_qs_model.pop_node_qs()


    @staticmethod
    def before_search_for_o2(parent_pv, search_context_model):
        (parent_pv.backwards_plot_model, parent_pv.is_terminate) = SearchRoutines.look_in_0_moves(
                info_depth              = INFO_DEPTH,
                parent_pv               = parent_pv,
                search_context_model    = search_context_model)


    @staticmethod
    def move_all_pv_o2(pv_list, search_context_model):
        """応手の開始。

        Parameters
        ----------
        pv_list : list<PrincipalVariationModel>
            ［読み筋］のリスト。

        Returns
        -------
        best_prot_model : BackwardsPlotModel
            最善の読み筋。
            これは駒得評価値も算出できる。
        """

        ####################
        # MARK: ノード訪問時
        ####################

        terminated_pv_list = []
        live_pv_list = []

        # best_pv             = None  # ベストな子
        # best_move           = None
        # best_move_cap_pt    = None

        # if search_context_model.gymnasium.is_mars:
        #     best_value = constants.value.BIG_VALUE
        # else:
        #     best_value = constants.value.SMALL_VALUE

        for pv in pv_list:

            ################################
            # MARK: 履歴の最後の一手を指す前
            ################################

            # my_move                         = pv.last_move_pv
            # cap_pt                          = pv.last_cap_pt_pv
            # piece_exchange_value_on_earth   = pv.last_value_pv

            ######################
            # MARK: 履歴を全部指す
            ######################

            SearchRoutines.do_move_vertical_all(pv=pv, search_context_model=search_context_model)

            ##################
            # MARK: 手番の処理
            ##################

            # ２階で探索不要なら。
            if pv.is_terminate:
                terminated_pv_list.append(pv)

            else:
                # ［水平指し手一覧］をクリーニング。
                remaining_moves = O3QuiescenceSearchRoutines.cleaning_horizontal_edges_o3a(parent_pv=pv, search_context_model=search_context_model)

                # ［駒を取る手］がないことを、［静止］と呼ぶ。
                if len(remaining_moves) == 0:
                    pv.backwards_plot_model = SearchRoutines.create_backwards_plot_model_at_quiescence(info_depth=INFO_DEPTH, search_context_model=search_context_model)
                    pv.is_terminate = True
                    terminated_pv_list.append(pv)

                else:
                    # remaining_moves から pv へ変換。
                    next_pv_list = SearchRoutines.convert_remaining_moves_to_pv_list(parent_pv=pv, remaining_moves=remaining_moves, search_context_model=search_context_model)
                    # TODO ３手目
                    next_pv.backwards_plot_model = O3QuiescenceSearchRoutines.search_as_quiescence_o3(
                            pv_list     = next_pv_list,
                            search_context_model    = search_context_model)

                    for next_pv in reversed(next_pv_list):
                        if next_pv.is_terminate:                    # ［読み筋］の探索が終了していれば。
                            terminated_pv_list.append(next_pv)      # 別のリストへ［読み筋］を退避します。
                        else:
                            live_pv_list.append(next_pv)

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

            # １階の手は、全ての手の読み筋を記憶します。最善手は選びません。
            pv.backwards_plot_model.append_move_from_back(
                    move                = pv.last_move_pv,
                    capture_piece_type  = pv.last_cap_pt_pv,
                    best_value          = pv.backwards_plot_model.get_exchange_value_on_earth(),
                    hint                = '')

            #(this_branch_value_on_earth, is_update_best) = SearchRoutines.is_update_best(best_pv=best_pv, child_plot_model=child_plot_model, piece_exchange_value_on_earth=piece_exchange_value_on_earth, search_context_model=search_context_model)

            # # 最善手の更新
            # if is_update_best:
            #     best_pv             = pv
            #     best_pv.backwards_plot_model    = child_plot_model
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
        # best_pv.backwards_plot_model.append_move_from_back(
        #         move                = best_move,
        #         capture_piece_type  = best_move_cap_pt,
        #         best_value          = best_value,
        #         hint                = '')

        return terminated_pv_list, live_pv_list


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
