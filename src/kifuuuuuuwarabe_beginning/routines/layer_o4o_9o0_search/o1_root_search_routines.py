import cshogi
import time

from ...models.layer_o1o0 import SquareModel
from ...models.layer_o5o0_search import SearchContextModel
from .search_routines import SearchRoutines
from .o2_counter_search_routines import O2CounterSearchRoutines


INFO_DEPTH = 1


class O1RootSearchRoutines(SearchRoutines):
    """１階の探索。
    """

    ######################################################
    # MARK: 一手も指さずに局面を見て、終局なら終局外を付加
    ######################################################

    @staticmethod
    def set_termination_if_it_o1(parent_pv, search_context_model):
        """一手も指さずに局面を見て、終局なら終局外を付加。
        手番が回ってきてから、終局が成立するものとする。（何も指さない手番）
        """
        (parent_pv.backwards_plot_model, parent_pv.is_terminate) = SearchRoutines.look_in_0_moves(
                info_depth              = INFO_DEPTH,
                parent_pv               = parent_pv,
                search_context_model    = search_context_model)


    @staticmethod
    def cleaning_horizontal_edges_o1(remaining_moves, parent_pv, search_context_model):
        """水平指し手をクリーニング。

        Parameters
        ----------
        parent_pv : PrincipalVariationModel
            親手。

        Returns
        -------
        remaining_moves : list<int>
            デバッグの都合。シーショーギの指し手のリスト。
        """

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

            # 一手も指さずに局面を見て、終局なら終局外を付加。
            O1RootSearchRoutines.set_termination_if_it_o1(parent_pv=pv, search_context_model=search_context_model)

            ######################
            # MARK: 履歴を全部戻す
            ######################

            SearchRoutines.undo_move_vertical_all(pv=pv, search_context_model=search_context_model)

            ##########################
            # MARK: 履歴を全部戻した後
            ##########################

            search_context_model.gymnasium.health_check_qs_model.pop_node_qs()


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

        ####################
        # MARK: ノード訪問時
        ####################

        terminated_pv_list = []
        live_pv_list = []

        for pv in pv_list:

            ######################
            # MARK: 履歴を全部指す
            ######################

            SearchRoutines.do_move_vertical_all(pv=pv, search_context_model=search_context_model)

            ##################
            # MARK: 手番の処理
            ##################

            # １階で探索不要なら。
            if pv.is_terminate:
                terminated_pv_list.append(pv)
            
            else:
                # ［水平指し手一覧］をクリーニング。
                remaining_moves = O2CounterSearchRoutines.cleaning_horizontal_edges_o2(parent_pv=pv, search_context_model=search_context_model)

                # ［駒を取る手］がないことを、［静止］と呼ぶ。
                if len(remaining_moves) == 0:
                    #TODO self._search_context_model.end_time = time.time()    # 計測終了時間
                    pv.backwards_plot_model = SearchRoutines.create_backwards_plot_model_at_quiescence(info_depth=INFO_DEPTH, search_context_model=search_context_model)
                    pv.is_terminate = True
                    terminated_pv_list.append(pv)
                
                else:
                    # remaining_moves から pv へ変換。
                    next_pv_list = SearchRoutines.convert_remaining_moves_to_pv_list(parent_pv=pv, remaining_moves=remaining_moves, search_context_model=search_context_model)

                    # TODO ２手目
                    # O2CounterSearchRoutines.extend_vertical_edges_o2(pv_list=next_pv_list, search_context_model=search_context_model)
                    # (terminated_pv_list, live_pv_list) = O2CounterSearchRoutines.move_all_pv_o2(
                    #         pv_list             = live_pv_list,
                    #         search_context_model= search_context_model)

                    # # 火星が嫌な手は削除。
                    # for terminated_pv in reversed(terminated_pv_list):
                    #     if 0 < terminated_pv.last_value_pv:
                    #         terminated_pv_list.remove(terminated_pv)
                    
                    # for live_pv in reversed(live_pv_list):
                    #     if 0 < live_pv.last_value_pv:
                    #         live_pv_list.remove(live_pv)

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
