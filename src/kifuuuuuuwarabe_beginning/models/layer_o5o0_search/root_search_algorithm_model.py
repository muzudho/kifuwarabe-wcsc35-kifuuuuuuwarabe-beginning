import cshogi
import time

from ..layer_o1o0 import constants, Mars, SquareModel
from .quiescence_search_algorithm_model import QuiescenceSearchAlgorithmModel
from .search_algorithm_model import SearchAlgorithmModel
from .counter_search_algorithm_model import CounterSearchAlgorithmModel
from .search_context_model import SearchContextModel


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


    def search_as_root(
            self,
            depth_qs,
            remaining_moves):
        """静止探索の開始。

        大まかにいって、１手目は全ての合法手を探索し、
        ２手目以降は、駒を取る手を中心に探索します。
        TODO できれば２手目も全ての合法手を探索したい。指した後取られる手があるから。

        Parameters
        ----------
        depth_qs : int
            静止探索で、あと何手深く読むか。
        remaining_moves : list<int>
            指し手のリスト。

        Returns
        -------
        all_backwards_plot_models_at_first : list<BackwardsPlotModel>
            全ての１階の合法手の読み筋。
        """

        self._search_context_model.start_time = time.time()          # 探索開始時間
        self._search_context_model.restart_time = self._search_context_model.start_time   # 前回の計測開始時間
        all_backwards_plot_models_at_first = []

        ########################
        # MARK: 指す前にやること
        ########################

        # 指さなくても分かること（ライブラリー使用）

        if self._search_context_model.gymnasium.table.is_game_over():
            """手番の投了局面時。
            """
            best_plot_model = self.create_backwards_plot_model_at_game_over()
            all_backwards_plot_models_at_first.append(best_plot_model)
            return all_backwards_plot_models_at_first

        # 一手詰めを詰める
        if not self._search_context_model.gymnasium.table.is_check():
            """手番玉に王手がかかっていない時で"""

            if (mate_move := self._search_context_model.gymnasium.table.mate_move_in_1ply()):
                """一手詰めの指し手があれば、それを取得"""
                best_plot_model = self.create_backwards_plot_model_at_mate_move_in_1_ply(mate_move=mate_move)
                all_backwards_plot_models_at_first.append(best_plot_model)
                return all_backwards_plot_models_at_first

        if self._search_context_model.gymnasium.table.is_nyugyoku():
            """手番の入玉宣言勝ち局面時。
            """
            best_plot_model = self.create_backwards_plot_model_at_nyugyoku_win()
            all_backwards_plot_models_at_first.append(best_plot_model)
            return all_backwards_plot_models_at_first

        # これ以上深く読まない場合。
        if depth_qs < 1:
            best_plot_model = self.create_backwards_plot_model_at_horizon(depth_qs)
            all_backwards_plot_models_at_first.append(best_plot_model)
            return all_backwards_plot_models_at_first

        # まだ深く読む場合。

        ######################
        # MARK: 合法手スキャン
        ######################

        # 最善手は探さなくていい。全部返すから。

        ############################
        # MARK: データ・クリーニング
        ############################

        remaining_moves = self.remove_depromoted_moves(remaining_moves=remaining_moves)       # ［成れるのに成らない手］は除外

        # ［駒を取る手］がないことを、［静止］と呼ぶ。
        if len(remaining_moves) == 0:
            best_plot_model = self.create_backwards_plot_model_at_quiescence(depth_qs=depth_qs)
            all_backwards_plot_models_at_first.append(best_plot_model)
            self._search_context_model.end_time = time.time()    # 計測終了時間
            return all_backwards_plot_models_at_first

        ####################
        # MARK: ノード訪問時
        ####################

        def set_controls(remaining_moves):
            """利きを記録
            """
            self._search_context_model.clear_root_searched_control_map()

            for my_move in remaining_moves:
                if cshogi.move_is_drop(my_move):
                    continue
                dst_sq_obj = SquareModel(cshogi.move_to(my_move))       # ［移動先マス］
                self._search_context_model.set_root_searched_control_map(sq=dst_sq_obj.sq, value=True)


        set_controls(remaining_moves=remaining_moves)

        for my_move in remaining_moves:

            ##################
            # MARK: 一手指す前
            ##################

            dst_sq_obj  = SquareModel(cshogi.move_to(my_move))      # ［移動先マス］
            # 打の場合、取った駒無し。空マス。
            cap_pt      = self._search_context_model.gymnasium.table.piece_type(dst_sq_obj.sq)    # 取った駒種類 NOTE 移動する前に、移動先の駒を取得すること。

            # １階呼出時は、どの手も無視しません。

            is_capture  = (cap_pt != cshogi.NONE)

            # ２階以降の呼出時は、駒を取る手でなければ無視。 FIXME 王手が絡んでいるとき、取れないこともあるから、王手が絡むときは場合分けしたい。
            if not is_capture:
                depth_qs_extend = 1    # ＜📚原則１＞により、駒を取らない手は、探索を１手延長します。
            else:
                depth_qs_extend = 0

            ################
            # MARK: 一手指す
            ################

            self._search_context_model.gymnasium.do_move_o1x(move = my_move)

            ####################
            # MARK: 一手指した後
            ####################

            self._search_context_model.number_of_visited_nodes  += 1
            depth_qs -= 1    # 深さを１下げる。
            self._search_context_model.frontwards_plot_model.append_move(
                    move    = my_move,
                    cap_pt  = cap_pt)
            self._search_context_model.gymnasium.health_check_qs_model.append_node(cshogi.move_to_usi(my_move))

            ####################
            # MARK: 相手番の処理
            ####################

            # NOTE この辺りは［１階］。max_depth - depth。

            search_context_model = SearchContextModel(
                    max_depth = depth_qs,
                    gymnasium = self._search_context_model.gymnasium)
            counter_search_algorithm_model = CounterSearchAlgorithmModel(            # 応手サーチ。
                    search_context_model = search_context_model)
            child_plot_model = counter_search_algorithm_model.search_as_normal(      # 再帰呼出
                    depth_qs       = depth_qs + depth_qs_extend)

            ################
            # MARK: 一手戻す
            ################

            self._search_context_model.gymnasium.undo_move_o1x()

            ####################
            # MARK: 一手戻した後
            ####################

            depth_qs += 1    # 深さを１上げる。
            self._search_context_model.frontwards_plot_model.pop_move()
            self._search_context_model.gymnasium.health_check_qs_model.pop_node()

            ##################
            # MARK: 手番の処理
            ##################

            # １階の手は、全ての手の読み筋を記憶します。最善手は選びません。
            child_plot_model.append_move(
                    move                = my_move,
                    capture_piece_type  = cap_pt,
                    hint                = '')   # f"１階の{Mars.japanese(self._search_context_model.gymnasium.is_mars)}の手はなんでも記憶"
            all_backwards_plot_models_at_first.append(child_plot_model)

            # NOTE この辺りは［０階］。

            # ベータカットもしません。全部返すから。

        ########################
        # MARK: 合法手スキャン後
        ########################

        # 指したい手がなかったなら、静止探索の末端局面の後ろだ。
        if len(all_backwards_plot_models_at_first) < 1:
            child_plot_model = self.create_backwards_plot_model_at_no_candidates(depth_qs=depth_qs)
            all_backwards_plot_models_at_first.append(child_plot_model)
            self._search_context_model.gymnasium.health_check_qs_model.on_out_of_termination('＜指したい手無し＞')

        self._search_context_model.end_time = time.time()    # 計測終了時間

        return all_backwards_plot_models_at_first
