import cshogi
import time

from ..layer_o1o_9o0 import PieceValuesModel
from ..layer_o1o0 import constants, Mars, PtolemaicTheoryModel, SquareModel
from ..layer_o1o0o_9o0_table_helper import TableHelper
from .search_algorithm_model import SearchAlgorithmModel


class QuiescenceSearchAlgorithmModel(SearchAlgorithmModel):
    """駒の取り合いのための静止探索。
    駒の取り合いが終わるまで、駒の取り合いを探索します。
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
    

    def search_alice(
            self,
            depth_qs,
            parent_move):
        """
        Parameters
        ----------
        depth : int
            あと何手深く読むか。
        parent_move : int
            １手前の手。

        Returns
        -------
        best_prot_model : BackwardsPlotModel
            最善の読み筋。
            これは駒得評価値も算出できる。
        """

        ########################
        # MARK: 指す前にやること
        ########################

        cur_time = time.time()                                          # 現在の時間
        erapsed_seconds = cur_time - self._search_context_model.restart_time    # 経過秒
        if 4 <= erapsed_seconds:                                        # 4秒以上経過してたら、情報出力
            print(f"info depth {self._search_context_model.max_depth - depth_qs} seldepth 0 time 1 nodes {self._search_context_model.number_of_visited_nodes} score cp 0 string thinking")
            self._search_context_model.restart_time = cur_time                   # 前回の計測時間を更新

        # 指さなくても分かること（ライブラリー使用）

        if self._search_context_model.gymnasium.table.is_game_over():
            """手番の投了局面時。
            """
            return self.create_backwards_plot_model_at_game_over()

        # 一手詰めを詰める
        if not self._search_context_model.gymnasium.table.is_check():
            """手番玉に王手がかかっていない時で"""

            if (mate_move := self._search_context_model.gymnasium.table.mate_move_in_1ply()):
                """一手詰めの指し手があれば、それを取得"""
                return self.create_backwards_plot_model_at_mate_move_in_1_ply(mate_move=mate_move)

        if self._search_context_model.gymnasium.table.is_nyugyoku():
            """手番の入玉宣言勝ち局面時。
            """
            return self.create_backwards_plot_model_at_nyugyoku_win()

        # これ以上深く読まない場合。
        if depth_qs < 1:
            return self.create_backwards_plot_model_at_horizon(depth_qs)

        # まだ深く読む場合。

        ######################
        # MARK: 合法手スキャン
        ######################

        # 合法手を全部調べる。
        legal_move_list = list(self._search_context_model.gymnasium.table.legal_moves)
        remaining_moves = legal_move_list

        ############################
        # MARK: データ・クリーニング
        ############################

        remaining_moves = self.remove_drop_moves(remaining_moves=remaining_moves)           # 打の手を全部除外したい。
        remaining_moves = self.remove_depromoted_moves(remaining_moves=remaining_moves)     # ［成れるのに成らない手］は除外
        (remaining_moves, rolled_back) = QuiescenceSearchAlgorithmModel.filtering_same_destination_move_list(parent_move=parent_move, remaining_moves=remaining_moves, rollback_if_empty=True) # できれば［同］の手を残す。
        remaining_moves = QuiescenceSearchAlgorithmModel.get_cheapest_move_list(remaining_moves=remaining_moves)
        (remaining_moves, rolled_back) = self.filtering_capture_or_mate(remaining_moves=remaining_moves, rollback_if_empty=False)       # 駒を取る手と、王手のみ残す

        # ［駒を取る手］がないことを、［静止］と呼ぶ。
        if len(remaining_moves) == 0:
            return self.create_backwards_plot_model_at_quiescence(depth_qs=depth_qs)

        ####################
        # MARK: ノード訪問時
        ####################

        best_plot_model     = None
        best_move           = None
        best_move_cap_pt    = None
        if self._search_context_model.gymnasium.is_mars:
            best_value = constants.value.BIG_VALUE
        else:
            best_value = constants.value.SMALL_VALUE
        depth_qs_extend     = 0

        for my_move in remaining_moves:

            ##################
            # MARK: 一手指す前
            ##################

            dst_sq_obj  = SquareModel(cshogi.move_to(my_move))      # ［移動先マス］
            cap_pt      = self._search_context_model.gymnasium.table.piece_type(dst_sq_obj.sq)    # 取った駒種類 NOTE 移動する前に、移動先の駒を取得すること。

            #     # ＜📚原則２＞ 王手は（駒を取らない手であっても）探索を続け、深さを１手延長する。
            #     if self._search_context_model.gymnasium.table.is_check():
            #         #depth_extend += 1  # FIXME 探索が終わらないくなる。
            #         pass

            ################
            # MARK: 一手指す
            ################

            self._search_context_model.gymnasium.do_move_o1x(move = my_move)

            ####################
            # MARK: 一手指した後
            ####################

            self._search_context_model.number_of_visited_nodes += 1
            depth_qs -= 1     # 深さを１下げる。
            self._search_context_model.frontwards_plot_model.append_move_from_front(
                    move    = my_move,
                    cap_pt  = cap_pt)
            self._search_context_model.gymnasium.health_check_qs_model.append_edge_qs(move=my_move, hint='')

            ####################
            # MARK: 相手番の処理
            ####################

            # NOTE ネガ・マックスではないので、評価値の正負を反転させなくていい。
            child_plot_model = self.search_alice(      # 再帰呼出
                    depth_qs       = depth_qs + depth_qs_extend,
                    parent_move = my_move)

            ################
            # MARK: 一手戻す
            ################

            self._search_context_model.gymnasium.undo_move_o1x()

            ####################
            # MARK: 一手戻した後
            ####################

            depth_qs += 1                 # 深さを１上げる。
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
                        
            # 最善手の更新（１つに絞る）
            if its_update_best:
                best_plot_model     = child_plot_model
                best_move           = my_move
                best_move_cap_pt    = cap_pt
                best_value          = this_branch_value_on_earth

        ########################
        # MARK: 合法手スキャン後
        ########################

        # 指したい手がなかったなら、静止探索の末端局面の後ろだ。
        if best_plot_model is None:
            return self.create_backwards_plot_model_at_no_candidates(depth_qs=depth_qs)

        # 読み筋に今回の手を付け加える。（ TODO 駒得点も付けたい）
        best_plot_model.append_move_from_back(
                move                = best_move,
                capture_piece_type  = best_move_cap_pt,
                best_value          = best_value,
                hint                = '')   # f"{self._search_context_model.max_depth - depth_qs + 1}階の{Mars.japanese(self._search_context_model.gymnasium.is_mars)}の手記憶"

        return best_plot_model


    def filtering_same_destination_move_list(parent_move, remaining_moves, rollback_if_empty):
        """［同］（１つ前の手の移動先に移動する手）を優先的に選ぶ。

        Returns
        -------
        move_list : list
            指し手のリスト。
        rolled_back : bool
            ロールバックされた。
        """
        dst_sq_of_parent_move_obj = SquareModel(cshogi.move_to(parent_move))      # ［１つ親の手］の［移動先マス］
        same_destination_move_list = []

        for my_move in remaining_moves:
            dst_sq_obj  = SquareModel(cshogi.move_to(my_move))      # ［移動先マス］
            if dst_sq_obj.sq == dst_sq_of_parent_move_obj.sq:
                same_destination_move_list.append(my_move)
        
        if 0 < len(same_destination_move_list):
            return same_destination_move_list, False
        
        if rollback_if_empty:
            return remaining_moves, True
        return [], False


    def get_cheapest_move_list(remaining_moves):
        """TODO 一番安い駒の指し手だけを選ぶ。
        TODO 打はどう扱う？
        """
        cheapest_value = constants.value.BIG_VALUE
        cheapest_move_list = []
        for my_move in remaining_moves:
            moving_pt = TableHelper.get_moving_pt_from_move(my_move)
            value = PieceValuesModel.by_piece_type(moving_pt)
            if value == cheapest_move_list:
                cheapest_move_list.append(my_move)
            elif value < cheapest_value:
                cheapest_value = value
                cheapest_move_list = [my_move]            
        return cheapest_move_list
