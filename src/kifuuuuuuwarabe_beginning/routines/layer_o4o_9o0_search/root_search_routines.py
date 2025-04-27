import cshogi
import time

from ...models.layer_o1o0 import SquareModel
from .search_routines import SearchRoutines
from .counter_search_routines import CounterSearchRoutines


class RootSearchRoutines(SearchRoutines):
    """１階の全てのリーガル・ムーブについて静止探索。
    """


    @staticmethod
    def search_after_entry_node_root(remaining_moves, parent_pv, search_context_model):
        """
        Returns
        -------
        remaining_moves : list<int>
            デバッグの都合。シーショーギの指し手のリスト。
        pv_list : list<PrincipalVariationModel>
            読み筋のリスト。
        """
        ##########################
        # MARK: 合法手クリーニング
        ##########################

        # 最善手は探さなくていい。全部返すから。
        remaining_moves = SearchRoutines.remove_depromoted_moves(remaining_moves=remaining_moves, search_context_model=search_context_model)       # ［成れるのに成らない手］は除外
        pv_list = SearchRoutines.convert_remaining_moves_to_pv_list(parent_pv=parent_pv, remaining_moves=remaining_moves, search_context_model=search_context_model)
        return pv_list


    @staticmethod
    def check_control_from_root(pv_list, search_context_model):

        ####################
        # MARK: ノード訪問時
        ####################

        RootSearchRoutines._set_controls(pv_list=pv_list, search_context_model=search_context_model)

        ################################
        # MARK: PVリスト探索（応手除く）
        ################################

        for pv in pv_list:
            ######################
            # MARK: 履歴を全部指す
            ######################

            SearchRoutines.do_move_vertical_all(pv=pv, search_context_model=search_context_model)

            ##########################
            # MARK: 履歴を全部指した後
            ##########################

            search_context_model.number_of_visited_nodes  += 1    # 開示情報
            search_context_model.gymnasium.health_check_qs_model.append_edge_qs(move=pv.vertical_list_of_move_pv[-1], hint='')    # ログ

            ####################
            # MARK: 相手番の処理
            ####################

            # PV を更新。
            (pv.backwards_plot_model, pv.is_terminate) = RootSearchRoutines._search_before_entering_counter_node(pv=pv, search_context_model=search_context_model)

            ######################
            # MARK: 履歴を全部戻す
            ######################

            SearchRoutines.undo_move_vertical_all(pv=pv, search_context_model=search_context_model)

            ##########################
            # MARK: 履歴を全部戻した後
            ##########################

            search_context_model.frontwards_plot_model.pop_move()
            search_context_model.gymnasium.health_check_qs_model.pop_node_qs()


    @staticmethod
    def visit_counter_from_root(pv_list, search_context_model):
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

        next_pv_list = []

        for pv in pv_list:

            ######################
            # MARK: 履歴を全部指す
            ######################

            SearchRoutines.do_move_vertical_all(pv=pv, search_context_model=search_context_model)

            ####################
            # MARK: 相手番の処理
            ####################

            # FIXME この処理は、幅優先探索に変えたい。

            if not pv.is_terminate:
                child_pv_list = CounterSearchRoutines.search_after_entry_node_counter(parent_pv=pv, search_context_model=search_context_model)

                for child_pv in reversed(child_pv_list):
                    if child_pv.is_terminate:           # ［読み筋］の探索が終了していれば。
                        next_pv_list.append(child_pv)        # 別のリストへ［読み筋］を退避します。
                        child_pv_list.remove(child_pv)

                # TODO 再帰しないようにしてほしい。
                pv.backwards_plot_model = CounterSearchRoutines.search_as_counter(pv_list=child_pv_list, search_context_model=search_context_model)       # 再帰呼出

            ######################
            # MARK: 履歴を全部戻す
            ######################

            SearchRoutines.undo_move_vertical_all(pv=pv, search_context_model=search_context_model)

            ##################
            # MARK: 手番の処理
            ##################

            # １階の手は、全ての手の読み筋を記憶します。最善手は選びません。
            pv.backwards_plot_model.append_move_from_back(
                    move                = pv.vertical_list_of_move_pv[-1],
                    capture_piece_type  = pv.vertical_list_of_cap_pt_pv[-1],
                    best_value          = pv.backwards_plot_model.get_exchange_value_on_earth(),
                    hint                = '')

            # ベータカットもしません。全部返すから。
            pv.value_pv += pv.backwards_plot_model.get_exchange_value_on_earth()
            next_pv_list.append(pv.copy_pv())

        ######################
        # MARK: PVリスト探索後
        ######################

        # 指し手が無いということはない。ゲームオーバー判定を先にしているから。

        pv_list = next_pv_list      # 入れ替え
        next_pv_list = []

        search_context_model.end_time = time.time()    # 計測終了時間
        return pv_list


    @staticmethod
    def _search_before_entering_counter_node(pv, search_context_model):
        """ノードに入る前に。

        Returns
        -------
        backwards_plot_model : BackwardsPlotModel
            読み筋。
        is_terminate : bool
            読み終わり。
        """

        ########################
        # MARK: 指す前にやること
        ########################

        search_context_model.start_time = time.time()          # 探索開始時間
        search_context_model.restart_time = search_context_model.start_time   # 前回の計測開始時間

        if search_context_model.gymnasium.table.is_game_over():
            """手番の投了局面時。
            """
            return SearchRoutines.create_backwards_plot_model_at_game_over(search_context_model=search_context_model), True

        # 一手詰めを詰める
        if not search_context_model.gymnasium.table.is_check():
            """手番玉に王手がかかっていない時で"""

            if (mate_move := search_context_model.gymnasium.table.mate_move_in_1ply()):
                """一手詰めの指し手があれば、それを取得"""
                return SearchRoutines.create_backwards_plot_model_at_mate_move_in_1_ply(mate_move=mate_move, search_context_model=search_context_model), True

        if search_context_model.gymnasium.table.is_nyugyoku():
            """手番の入玉宣言勝ち局面時。
            """
            return SearchRoutines.create_backwards_plot_model_at_nyugyoku_win(search_context_model=search_context_model), True

        return pv.backwards_plot_model, pv.is_terminate


    @staticmethod
    def _set_controls(pv_list, search_context_model):
        """利きを記録
        """
        search_context_model.clear_root_searched_control_map()

        for pv in pv_list:
            my_move = pv.vertical_list_of_move_pv[-1]
            if cshogi.move_is_drop(my_move):
                continue
            dst_sq_obj = SquareModel(cshogi.move_to(my_move))       # ［移動先マス］
            search_context_model.set_root_searched_control_map(sq=dst_sq_obj.sq, value=True)
