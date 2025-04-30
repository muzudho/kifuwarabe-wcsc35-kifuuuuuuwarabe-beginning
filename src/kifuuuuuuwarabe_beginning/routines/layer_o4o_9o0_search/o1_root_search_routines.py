import cshogi
import time

from ...models.layer_o1o0 import SquareModel
from ...models.layer_o5o0_search import SearchContextModel
from .search_routines import SearchRoutines
from .o2_counter_search_routines import O2CounterSearchRoutines


INFO_DEPTH = 1


class O1RootSearchRoutines(SearchRoutines):
    """１階の全てのリーガル・ムーブについて静止探索。
    """


    @staticmethod
    def cleaning_horizontal_edges_o1(remaining_moves, parent_pv, search_context_model):
        """水平指し手をクリーニング。

        Returns
        -------
        remaining_moves : list<int>
            デバッグの都合。シーショーギの指し手のリスト。
        pv_list : list<PrincipalVariationModel>
            読み筋のリスト。
        """

        # 最善手は探さなくていい。全部返すから。
        remaining_moves = SearchRoutines.remove_depromoted_moves(remaining_moves=remaining_moves, search_context_model=search_context_model)       # ［成れるのに成らない手］は除外
        return remaining_moves


    @staticmethod
    def extend_vertical_edges_o1(pv_list, search_context_model):
        """縦の辺を伸ばす。
        """

        ####################
        # MARK: ノード訪問時
        ####################

        O1RootSearchRoutines._set_controls(pv_list=pv_list, search_context_model=search_context_model)

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

            search_context_model.number_of_visited_nodes  += 1    # 開示情報
            search_context_model.gymnasium.health_check_qs_model.append_edge_qs(move=my_move, cap_pt=cap_pt, value=piece_exchange_value_on_earth, comment='')    # ログ

            ####################
            # MARK: 相手番の処理
            ####################

            search_context_model.start_time = time.time()          # 探索開始時間
            search_context_model.restart_time = search_context_model.start_time   # 前回の計測開始時間

            # PV を更新。
            O1RootSearchRoutines.before_search_for_o1(parent_pv=pv, search_context_model=search_context_model)

            ######################
            # MARK: 履歴を全部戻す
            ######################

            SearchRoutines.undo_move_vertical_all(pv=pv, search_context_model=search_context_model)

            ##########################
            # MARK: 履歴を全部戻した後
            ##########################

            search_context_model.gymnasium.health_check_qs_model.pop_node_qs()


    @staticmethod
    def before_search_for_o1(parent_pv, search_context_model):
        (parent_pv.backwards_plot_model, parent_pv.is_terminate) = SearchRoutines.look_in_0_moves(
                info_depth              = INFO_DEPTH,
                parent_pv               = parent_pv,
                search_context_model    = search_context_model)


    @staticmethod
    def move_all_pv_o1(pv_list, search_context_model):
        """通常探索の開始。

        Parameters
        ----------
        pv_list : list<PrincipalVariationModel>
            ［読み筋］のリスト。

        Returns
        -------
        pv_list : list<PrincipalVariationModel>
            有力な読み筋。棋譜のようなもの。
            枝が増えて、合法手の数より多くなることがあることに注意。
        """

        # まだ深く読む場合。

        ################################
        # MARK: PVリスト探索（応手）
        ################################

        terminated_pv_list = []
        live_pv_list = []

        for pv in pv_list:

            ######################
            # MARK: 履歴を全部指す
            ######################

            SearchRoutines.do_move_vertical_all(pv=pv, search_context_model=search_context_model)

            ####################
            # MARK: 相手番の処理
            ####################

            # １階で探索不要なら。
            if pv.is_terminate:
                terminated_pv_list.append(pv)
            
            else:
                # ［水平指し手一覧］をクリーニング。
                remaining_moves = O2CounterSearchRoutines.cleaning_horizontal_edges_o2(parent_pv=pv, search_context_model=search_context_model)

                # ［駒を取る手］がないことを、［静止］と呼ぶ。
                if len(remaining_moves) == 0:
                    #TODO self._search_context_model.end_time = time.time()    # 計測終了時間
                    pv.backwards_plot_model = SearchContextModel.create_backwards_plot_model_at_quiescence(info_depth=O1RootSearchRoutines.INFO_DEPTH, search_context_model=search_context_model)
                    pv.is_terminate = True
                    terminated_pv_list.append(pv)
                
                else:
                    # remaining_moves から pv へ変換。
                    next_pv_list = SearchRoutines.convert_remaining_moves_to_pv_list(parent_pv=pv, remaining_moves=remaining_moves, search_context_model=search_context_model)

                    for next_pv in reversed(next_pv_list):
                        # TODO ２手目
                        #next_pv.backwards_plot_model = O2CounterSearchRoutines.search_as_o2(pv_list=live_pv_list, search_context_model=search_context_model)

                        if next_pv.is_terminate:                    # ［読み筋］の探索が終了していれば。
                            terminated_pv_list.append(next_pv)      # 別のリストへ［読み筋］を退避します。
                        else:
                            live_pv_list.append(next_pv)

            ######################
            # MARK: 履歴を全部戻す
            ######################

            SearchRoutines.undo_move_vertical_all(pv=pv, search_context_model=search_context_model)

            ##################
            # MARK: 手番の処理
            ##################

            # １階の手は、全ての手の読み筋を記憶します。最善手は選びません。
            pv.backwards_plot_model.append_move_from_back(
                    move                = pv.last_move_pv,
                    capture_piece_type  = pv.last_cap_pt_pv,
                    best_value          = pv.backwards_plot_model.get_exchange_value_on_earth(),
                    hint                = '')

            # ベータカットもしません。全部返すから。
            #pv.value_pv += pv.backwards_plot_model.get_exchange_value_on_earth()
            #terminated_pv_list.append(pv.copy_pv())

        ######################
        # MARK: PVリスト探索後
        ######################

        # 指し手が無いということはない。ゲームオーバー判定を先にしているから。

        search_context_model.end_time = time.time()    # 計測終了時間
        return terminated_pv_list, live_pv_list


    @staticmethod
    def _set_controls(pv_list, search_context_model):
        """利きを記録
        """
        search_context_model.clear_root_searched_control_map()

        for pv in pv_list:
            my_move = pv.last_move_pv
            if cshogi.move_is_drop(my_move):
                continue
            dst_sq_obj = SquareModel(cshogi.move_to(my_move))       # ［移動先マス］
            search_context_model.set_root_searched_control_map(sq=dst_sq_obj.sq, value=True)
