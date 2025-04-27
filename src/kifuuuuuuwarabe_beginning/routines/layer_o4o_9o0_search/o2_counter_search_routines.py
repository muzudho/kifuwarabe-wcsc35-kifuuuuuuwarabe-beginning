import cshogi
import time

from ...models.layer_o1o_9o0 import PieceValuesModel
from ...models.layer_o1o0 import constants, SquareModel
from .search_routines import SearchRoutines
from .o3_quiescence_search_routines import O3QuiescenceSearchRoutines


class O2CounterSearchRoutines(SearchRoutines):
    """２階の探索。
    """


    @staticmethod
    def cleaning_horizontal_edges_counter(parent_pv, search_context_model):
        """
        Parameters
        ----------
        parent_pv : PrincipalVariationModel
            親手。

        Returns
        -------
        pv_list : list<PrincipalVariationModel>
            読み筋のリスト。
        """
        if parent_pv.is_terminate:
            return []

        ##########################
        # MARK: 合法手クリーニング
        ##########################
        
        remaining_moves = list(search_context_model.gymnasium.table.legal_moves)      # 全合法手。
        remaining_moves = SearchRoutines.remove_depromoted_moves(remaining_moves=remaining_moves, search_context_model=search_context_model)     # ［成れるのに成らない手］は除外
        aigoma_move_list = O2CounterSearchRoutines._choice_aigoma_move_list(remaining_moves=remaining_moves, search_context_model=search_context_model)   # ［間駒］（相手の利きの上に置く手）を抽出。
        remaining_moves = O2CounterSearchRoutines._remove_drop_except_aigoma(remaining_moves)  # ［間駒］以外の［打］は（多すぎるので）除外。
        (remaining_moves, rolled_back) = SearchRoutines.filtering_capture_or_mate(remaining_moves=remaining_moves, rollback_if_empty=True, search_context_model=search_context_model)    # ［カウンター探索］では、駒を取る手と、王手のみ残す。［駒を取る手、王手］が無ければ、（巻き戻して）それ以外の手を指します。
        remaining_moves.extend(aigoma_move_list)

        # remaining_moves から pv へ変換。
        pv_list = SearchRoutines.convert_remaining_moves_to_pv_list(parent_pv=parent_pv, remaining_moves=remaining_moves, search_context_model=search_context_model)
        return pv_list


    @staticmethod
    def search_as_counter(pv_list, search_context_model):
        """応手の開始。

        Parameters
        ----------
        pass

        Returns
        -------
        best_prot_model : BackwardsPlotModel
            最善の読み筋。
            これは駒得評価値も算出できる。
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

            my_move = pv.vertical_list_of_move_pv[-1]
            cap_pt  = pv.vertical_list_of_cap_pt_pv[-1]

            # NOTE `earth` - 自分。 `mars` - 対戦相手。
            piece_exchange_value_on_earth = PieceValuesModel.get_piece_exchange_value_on_earth(      # 交換値に変換。正の数とする。
                    pt          = cap_pt,
                    is_mars     = search_context_model.gymnasium.is_mars)

            ##############################
            # MARK: 履歴の最後の一手を指す
            ##############################

            search_context_model.gymnasium.do_move_o1x(move = my_move)

            ##################################
            # MARK: 履歴の最後の一手を指した後
            ##################################

            search_context_model.number_of_visited_nodes  += 1
            search_context_model.frontwards_plot_model.append_move_from_front(
                    move    = my_move,
                    cap_pt  = cap_pt)
            search_context_model.gymnasium.health_check_qs_model.append_edge_qs(move=my_move, hint='')

            ####################
            # MARK: 相手番の処理
            ####################

            # TODO 静止探索は後回しにしたい。
            
            (pv.backwards_plot_model, pv.is_terminate) = O3QuiescenceSearchRoutines.search_before_entering_quiescence_node(
                    depth_qs    = search_context_model.max_depth_qs,
                    pv          = pv,
                    parent_move = my_move,
                    search_context_model    = search_context_model)
            
            if pv.is_terminate:
                child_plot_model = pv.backwards_plot_model
            else:
                if not pv.is_terminate:
                    child_pv_list = O3QuiescenceSearchRoutines.cleaning_horizontal_edges_quiescence(parent_pv=pv, search_context_model=search_context_model)

                    # ［駒を取る手］がないことを、［静止］と呼ぶ。
                    if len(child_pv_list) == 0:
                        pv.backwards_plot_model = SearchRoutines.create_backwards_plot_model_at_quiescence(depth_qs=-1, search_context_model=search_context_model)
                        pv.is_terminate = True

                if not pv.is_terminate:
                    child_plot_model = O3QuiescenceSearchRoutines.search_as_quiescence(      # 再帰呼出
                            depth_qs    = search_context_model.max_depth_qs,
                            pv_list     = child_pv_list,
                            search_context_model    = search_context_model)
                else:
                    child_plot_model = pv.backwards_plot_model

            ##############################
            # MARK: 履歴の最後の一手を戻す
            ##############################

            search_context_model.gymnasium.undo_move_o1x()

            ##################################
            # MARK: 履歴の最後の一手を戻した後
            ##################################

            search_context_model.frontwards_plot_model.pop_move()
            search_context_model.gymnasium.health_check_qs_model.pop_node_qs()

            ##################
            # MARK: 手番の処理
            ##################

            (this_branch_value_on_earth, is_update_best) = SearchRoutines.is_update_best(best_pv=best_pv, child_plot_model=child_plot_model, piece_exchange_value_on_earth=piece_exchange_value_on_earth, search_context_model=search_context_model)

            # 最善手の更新
            if is_update_best:
                best_pv             = pv
                best_pv.backwards_plot_model    = child_plot_model
                best_move           = my_move
                best_move_cap_pt    = cap_pt
                best_value          = this_branch_value_on_earth

            # ベータカットもしません。全部返すから。

        ########################
        # MARK: 合法手スキャン後
        ########################

        # 指したい手がなかったなら、静止探索の末端局面の後ろだ。
        if best_pv is None:
            return SearchRoutines.create_backwards_plot_model_at_no_candidates(depth_qs=-1, search_context_model=search_context_model)

        # 今回の手を付け加える。
        best_pv.backwards_plot_model.append_move_from_back(
                move                = best_move,
                capture_piece_type  = best_move_cap_pt,
                best_value          = best_value,
                hint                = '')

        search_context_model.end_time = time.time()    # 計測終了時間

        return best_pv.backwards_plot_model


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
