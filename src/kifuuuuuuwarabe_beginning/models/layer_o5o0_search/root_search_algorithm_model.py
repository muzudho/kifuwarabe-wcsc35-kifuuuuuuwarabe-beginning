import cshogi
import time

from ..layer_o1o_9o0 import PieceValuesModel
from ..layer_o1o0 import constants, Mars, SquareModel
from .search_algorithm_model import SearchAlgorithmModel
from .counter_search_algorithm_model import CounterSearchAlgorithmModel
from .principal_variation_model import PrincipalVariationModel


class RootSearchAlgorithmModel(SearchAlgorithmModel):
    """１階の全てのリーガル・ムーブについて静止探索。
    """


    def __init__(self, search_context_model):
        """
        Parameters
        ----------
        search_context_model : SearchContextModel
            探索モデル。
        """
        super().__init__(
                search_context_model=search_context_model)


    def search_before_entry_node(self, pv):
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

        self._search_context_model.start_time = time.time()          # 探索開始時間
        self._search_context_model.restart_time = self._search_context_model.start_time   # 前回の計測開始時間

        # 指さなくても分かること（ライブラリー使用）

        if self._search_context_model.gymnasium.table.is_game_over():
            """手番の投了局面時。
            """
            return self.create_backwards_plot_model_at_game_over(), True

        # 一手詰めを詰める
        if not self._search_context_model.gymnasium.table.is_check():
            """手番玉に王手がかかっていない時で"""

            if (mate_move := self._search_context_model.gymnasium.table.mate_move_in_1ply()):
                """一手詰めの指し手があれば、それを取得"""
                return self.create_backwards_plot_model_at_mate_move_in_1_ply(mate_move=mate_move), True

        if self._search_context_model.gymnasium.table.is_nyugyoku():
            """手番の入玉宣言勝ち局面時。
            """
            return self.create_backwards_plot_model_at_nyugyoku_win(), True

        return pv.backwards_plot_model, False


    def search_after_entry_node_counter(self, parent_pv):
        pass


    def search_as_root(
            self,
            remaining_moves):
        """静止探索の開始。

        大まかにいって、１手目は全ての合法手を探索し、
        ２手目以降は、駒を取る手を中心に探索します。
        TODO できれば２手目も全ての合法手を探索したい。指した後取られる手があるから。

        Parameters
        ----------
        remaining_moves : list<int>
            指し手のリスト。

        Returns
        -------
        pv_list : list<PrincipalVariationModel>
            有力な読み筋。棋譜のようなもの。
            枝が増えて、合法手の数より多くなることがあることに注意。
        """

        # まだ深く読む場合。

        ##########################
        # MARK: 合法手クリーニング
        ##########################

        # 最善手は探さなくていい。全部返すから。

        remaining_moves = self.remove_depromoted_moves(remaining_moves=remaining_moves)       # ［成れるのに成らない手］は除外

        # ［駒を取る手］がないことを、［静止］と呼ぶ。
        if len(remaining_moves) == 0:
            self._search_context_model.end_time = time.time()    # 計測終了時間
            backwards_plot_model=self.create_backwards_plot_model_at_quiescence(depth_qs=-1)
            return [PrincipalVariationModel(vertical_list_of_move_pv=[], vertical_list_of_cap_pt_pv=[], value_pv=backwards_plot_model.get_exchange_value_on_earth(), backwards_plot_model=backwards_plot_model)]

        ####################
        # MARK: ノード訪問時
        ####################

        RootSearchAlgorithmModel._set_controls(remaining_moves=remaining_moves, search_context_model=self._search_context_model)

        pv_list = RootSearchAlgorithmModel._make_pv_list(remaining_moves=remaining_moves, search_context_model=self._search_context_model)

        ####################
        # MARK: PVリスト探索
        ####################

        next_pv_list = []

        for pv in pv_list:
            vertical_list_of_move_pv = pv.pop_vertical_list_of_move_pv()      # 指し手の履歴をポップします。

            ########################
            # MARK: 履歴を全部指す前
            ########################

            # TODO 駒を取った計算はパス。

            ######################
            # MARK: 履歴を全部指す
            ######################

            last_child_move = None
            for my_move in vertical_list_of_move_pv:
                self._search_context_model.gymnasium.do_move_o1x(move = my_move)
                last_child_move = my_move

            ##########################
            # MARK: 履歴を全部指した後
            ##########################

            self._search_context_model.number_of_visited_nodes  += 1
            self._search_context_model.gymnasium.health_check_qs_model.append_edge_qs(move=last_child_move, hint='')

            ####################
            # MARK: 相手番の処理
            ####################

            # FIXME この処理は、幅優先探索に変えたい。

            counter_search_algorithm_model = CounterSearchAlgorithmModel(            # 応手サーチ。
                    search_context_model = self._search_context_model)
            (pv.backwards_plot_model, pv.is_terminate) = counter_search_algorithm_model.search_before_entry_node(pv=pv)

            if not pv.is_terminate:
                child_pv_list = counter_search_algorithm_model.search_after_entry_node_counter(parent_pv=pv)

                for child_pv in reversed(child_pv_list):
                    if child_pv.is_terminate:           # ［読み筋］の探索が終了していれば。
                        next_pv_list.append(child_pv)        # 別のリストへ［読み筋］を退避します。
                        child_pv_list.remove(child_pv)

                pv.backwards_plot_model = counter_search_algorithm_model.search_as_counter(pv_list=child_pv_list)       # 再帰呼出

            ######################
            # MARK: 履歴を全部戻す
            ######################

            for i in range(0, len(vertical_list_of_move_pv)):
                self._search_context_model.gymnasium.undo_move_o1x()

            ##########################
            # MARK: 履歴を全部戻した後
            ##########################

            self._search_context_model.frontwards_plot_model.pop_move()
            self._search_context_model.gymnasium.health_check_qs_model.pop_node_qs()

            ##################
            # MARK: 手番の処理
            ##################

            # １階の手は、全ての手の読み筋を記憶します。最善手は選びません。
            pv.backwards_plot_model.append_move_from_back(
                    move                = last_child_move,
                    capture_piece_type  = pv.vertical_list_of_cap_pt_pv[-1],
                    best_value          = pv.backwards_plot_model.get_exchange_value_on_earth(),
                    hint                = '')

            # ベータカットもしません。全部返すから。
            pv.value_pv += pv.backwards_plot_model.get_exchange_value_on_earth()
            next_pv_list.append(pv.copy_pv())

        ########################
        # MARK: 合法手スキャン後
        ########################

        # 指し手が無いということはない。ゲームオーバー判定を先にしているから。

        self._search_context_model.end_time = time.time()    # 計測終了時間
        return next_pv_list


    def _make_pv_list(remaining_moves, search_context_model):
        """PVリスト作成。
        """
        pv_list = []

        # 準備。
        for my_move in remaining_moves:

            # （あれば）駒を取る。
            dst_sq_obj  = SquareModel(cshogi.move_to(my_move))      # ［移動先マス］
            cap_pt      = search_context_model.gymnasium.table.piece_type(dst_sq_obj.sq)    # ［移動先マス］にある［駒種類］。つまりそれは取った駒。打の［移動先マス］は常に空きマス。
            is_capture  = (cap_pt != cshogi.NONE)

            pv = PrincipalVariationModel(vertical_list_of_move_pv=[my_move], vertical_list_of_cap_pt_pv=[cap_pt], value_pv=0, backwards_plot_model=None)

            # （取っていれば）取った駒の点数計算。
            if is_capture:
                # NOTE `earth` - 自分。 `mars` - 対戦相手。
                pv.value_pv += PieceValuesModel.get_piece_exchange_value_on_earth(      # 交換値に変換。正の数とする。
                        pt          = cap_pt,
                        is_mars     = search_context_model.gymnasium.is_mars)
            else:
                pv.value_pv += 0

            pv_list.append(pv)

            search_context_model.frontwards_plot_model.append_move_from_front(
                    move    = my_move,
                    cap_pt  = cap_pt)

        return pv_list


    def _set_controls(remaining_moves, search_context_model):
        """利きを記録
        """
        search_context_model.clear_root_searched_control_map()

        for my_move in remaining_moves:
            if cshogi.move_is_drop(my_move):
                continue
            dst_sq_obj = SquareModel(cshogi.move_to(my_move))       # ［移動先マス］
            search_context_model.set_root_searched_control_map(sq=dst_sq_obj.sq, value=True)
