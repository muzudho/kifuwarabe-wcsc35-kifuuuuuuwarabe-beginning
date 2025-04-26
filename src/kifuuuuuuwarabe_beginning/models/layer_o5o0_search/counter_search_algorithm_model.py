import cshogi
import time

from ..layer_o1o_9o0 import PieceValuesModel
from ..layer_o1o0 import constants, Mars, PtolemaicTheoryModel, SquareModel
from .quiescence_search_algorithm_model import QuiescenceSearchAlgorithmModel
from .search_algorithm_model import SearchAlgorithmModel


class CounterSearchAlgorithmModel(SearchAlgorithmModel):
    """２階の探索。
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


    def search_as_normal(
            self):
        """静止探索の開始。

        大まかにいって、１手目は全ての合法手を探索し、
        ２手目以降は、駒を取る手を中心に探索します。
        TODO できれば２手目も全ての合法手を探索したい。指した後取られる手があるから。

        Parameters
        ----------
        pass

        Returns
        -------
        best_prot_model : BackwardsPlotModel
            最善の読み筋。
            これは駒得評価値も算出できる。
        """

        self._search_context_model.start_time = time.time()          # 探索開始時間
        self._search_context_model.restart_time = self._search_context_model.start_time   # 前回の計測開始時間

        ########################
        # MARK: 指す前にやること
        ########################

        # 指さなくても分かること（ライブラリー使用）

        if self._search_context_model.gymnasium.table.is_game_over():
            """手番の投了局面時。
            """
            best_plot_model = self.create_backwards_plot_model_at_game_over()
            return best_plot_model

        # 一手詰めを詰める
        if not self._search_context_model.gymnasium.table.is_check():
            """手番玉に王手がかかっていない時で"""

            if (mate_move := self._search_context_model.gymnasium.table.mate_move_in_1ply()):
                """一手詰めの指し手があれば、それを取得"""
                best_plot_model = self.create_backwards_plot_model_at_mate_move_in_1_ply(mate_move=mate_move)
                return best_plot_model

        if self._search_context_model.gymnasium.table.is_nyugyoku():
            """手番の入玉宣言勝ち局面時。
            """
            best_plot_model = self.create_backwards_plot_model_at_nyugyoku_win()
            return best_plot_model

        # # これ以上深く読まない場合。
        # if depth_qs < 1:
        #     best_plot_model = self.create_backwards_plot_model_at_horizon(depth_qs)
        #     return best_plot_model

        # まだ深く読む場合。

        ######################
        # MARK: 合法手スキャン
        ######################

        best_plot_model     = None
        best_move           = None
        best_move_cap_pt    = None

        # 合法手を全部調べる。
        legal_move_list = list(self._search_context_model.gymnasium.table.legal_moves)
        remaining_moves = legal_move_list

        ############################
        # MARK: データ・クリーニング
        ############################

        remaining_moves = self.remove_depromoted_moves(remaining_moves=remaining_moves)       # ［成れるのに成らない手］は除外

        aigoma_move_list = self._choice_aigoma_move_list(remaining_moves=remaining_moves)    # ［間駒］（相手の利きの上に置く手）を抽出。

        # TODO ［間駒］以外の［打］は（多すぎるので）除外。
        for my_move in reversed(remaining_moves):
            is_drop = cshogi.move_is_drop(my_move)
            if is_drop:
                remaining_moves.remove(my_move)

        (remaining_moves, rolled_back) = self.filtering_capture_or_mate(    # 駒を取る手と、王手のみ残す
                remaining_moves=remaining_moves,
                rollback_if_empty=True)     # ［カウンター探索］では、［駒を取る手、王手］が無ければ、（巻き戻して）それ以外の手を指します。

        remaining_moves.extend(aigoma_move_list)

        # ［駒を取る手］がないことを、［静止］と呼ぶ。
        if len(remaining_moves) == 0:
            best_plot_model = self.create_backwards_plot_model_at_quiescence(depth_qs=-1)
            self._search_context_model.end_time = time.time()    # 計測終了時間
            return best_plot_model

        ####################
        # MARK: ノード訪問時
        ####################

        if self._search_context_model.gymnasium.is_mars:
            best_value = constants.value.BIG_VALUE
        else:
            best_value = constants.value.SMALL_VALUE

        for my_move in remaining_moves:

            ##################
            # MARK: 一手指す前
            ##################

            # 打の場合、取った駒無し。空マス。
            dst_sq_obj  = SquareModel(cshogi.move_to(my_move))      # ［移動先マス］
            cap_pt      = self._search_context_model.gymnasium.table.piece_type(dst_sq_obj.sq)    # 取った駒種類 NOTE 移動する前に、移動先の駒を取得すること。

            ################
            # MARK: 一手指す
            ################

            self._search_context_model.gymnasium.do_move_o1x(move = my_move)

            ####################
            # MARK: 一手指した後
            ####################

            self._search_context_model.number_of_visited_nodes  += 1
            self._search_context_model.frontwards_plot_model.append_move_from_front(
                    move    = my_move,
                    cap_pt  = cap_pt)
            self._search_context_model.gymnasium.health_check_qs_model.append_edge_qs(move=my_move, hint='')

            ####################
            # MARK: 相手番の処理
            ####################

            quiescence_search_algorithum_model = QuiescenceSearchAlgorithmModel(    # 静止探索。
                    search_context_model    = self._search_context_model)
            child_plot_model = quiescence_search_algorithum_model.search_alice(      # 再帰呼出
                    depth_qs    = self._search_context_model.max_depth_qs,
                    parent_move = my_move)

            ################
            # MARK: 一手戻す
            ################

            self._search_context_model.gymnasium.undo_move_o1x()

            ####################
            # MARK: 一手戻した後
            ####################

            self._search_context_model.frontwards_plot_model.pop_move()
            self._search_context_model.gymnasium.health_check_qs_model.pop_node_qs()

            ##################
            # MARK: 手番の処理
            ##################

            its_update_best = False

            # NOTE `earth` - 自分。 `mars` - 対戦相手。
            piece_exchange_value_on_earth = PieceValuesModel.get_piece_exchange_value_on_earth(      # 交換値に変換。正の数とする。
                    pt          = cap_pt,
                    is_mars     = self._search_context_model.gymnasium.is_mars)

            # この枝の点（将来の点＋取った駒の点）
            this_branch_value_on_earth = child_plot_model.get_exchange_value_on_earth() + piece_exchange_value_on_earth

            # この枝が長兄なら。
            if best_plot_model is None:
                old_sibling_value = 0
            else:
                # 兄枝のベスト評価値
                old_sibling_value = best_plot_model.get_exchange_value_on_earth()     # とりあえず最善の読み筋の点数。

            (a, b) = self._search_context_model.gymnasium.ptolemaic_theory_model.swap(old_sibling_value, this_branch_value_on_earth)
            its_update_best = (a < b)

            # 最善手の更新
            if its_update_best:
                best_plot_model     = child_plot_model
                best_move           = my_move
                best_move_cap_pt    = cap_pt
                best_value          = this_branch_value_on_earth

            # ベータカットもしません。全部返すから。

        ########################
        # MARK: 合法手スキャン後
        ########################

        # 指したい手がなかったなら、静止探索の末端局面の後ろだ。
        if best_plot_model is None:
            return self.create_backwards_plot_model_at_no_candidates(depth_qs=-1)

        self._search_context_model.end_time = time.time()    # 計測終了時間

        # 今回の手を付け加える。
        best_plot_model.append_move_from_back(
                move                = best_move,
                capture_piece_type  = best_move_cap_pt,
                best_value          = best_value,
                hint                = '')

        return best_plot_model


    def _choice_aigoma_move_list(self, remaining_moves):
        # TODO ［間駒］（相手の利きの上に置く手）を抽出。
        aigoma_move_list = []
        for my_move in remaining_moves:
            dst_sq_obj  = SquareModel(cshogi.move_to(my_move))      # ［移動先マス］
            is_aigoma = self._search_context_model.get_root_searched_control_map(sq=dst_sq_obj.sq)
            if is_aigoma:
                aigoma_move_list.append(my_move)
        return aigoma_move_list
