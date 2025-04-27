import cshogi
import time

from ...models.layer_o1o_9o0 import PieceValuesModel
from ...models.layer_o1o0 import constants, SquareModel
from ...models.layer_o1o0o_9o0_table_helper import TableHelper
from .search_routines import SearchRoutines


class O5zQuiescenceSearchRoutines(SearchRoutines):
    """駒の取り合いのための静止探索。
    駒の取り合いが終わるまで、駒の取り合いを探索します。
    """


    @staticmethod
    def search_before_entering_quiescence_node(depth_qs, pv, parent_move, search_context_model):
        """
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

        cur_time = time.time()                                          # 現在の時間
        erapsed_seconds = cur_time - search_context_model.restart_time    # 経過秒
        if 4 <= erapsed_seconds:                                        # 4秒以上経過してたら、情報出力
            # ［ルート探索］、［カウンター探索］の２を足している。
            print(f"info depth {2 + search_context_model.max_depth_qs - depth_qs} seldepth 0 time 1 nodes {search_context_model.number_of_visited_nodes} score cp 0 string thinking")
            search_context_model.restart_time = cur_time                   # 前回の計測時間を更新

        # 指さなくても分かること（ライブラリー使用）

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

        # これ以上深く読まない場合。
        if depth_qs < 1:
            return SearchRoutines.create_backwards_plot_model_at_horizon(depth_qs, search_context_model=search_context_model), True

        return pv.backwards_plot_model, pv.is_terminate


    @staticmethod
    def search_as_quiescence(depth_qs, pv_list, search_context_model):
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
        depth_qs_extend     = 0

        for pv in pv_list:

            ################################
            # MARK: 履歴の最後の一手を指す前
            ################################

            my_move = pv.vertical_list_of_move_pv[-1]
            cap_pt  = pv.vertical_list_of_cap_pt_pv[-1]

            #     # ＜📚原則２＞ 王手は（駒を取らない手であっても）探索を続け、深さを１手延長する。
            #     if search_context_model.gymnasium.table.is_check():
            #         #depth_extend += 1  # FIXME 探索が終わらないくなる。
            #         pass

            # NOTE `earth` - 自分。 `mars` - 対戦相手。
            piece_exchange_value_on_earth = PieceValuesModel.get_piece_exchange_value_on_earth(      # 交換値に変換。正の数とする。
                    pt          = cap_pt,
                    is_mars     = search_context_model.gymnasium.is_mars)

            ################
            # MARK: 一手指す
            ################

            search_context_model.gymnasium.do_move_o1x(move = my_move)

            ####################
            # MARK: 一手指した後
            ####################

            search_context_model.number_of_visited_nodes += 1
            depth_qs -= 1     # 深さを１下げる。
            search_context_model.frontwards_plot_model.append_move_from_front(
                    move    = my_move,
                    cap_pt  = cap_pt)
            search_context_model.gymnasium.health_check_qs_model.append_edge_qs(move=my_move, hint='')

            ####################
            # MARK: 相手番の処理
            ####################

            # NOTE ネガ・マックスではないので、評価値の正負を反転させなくていい。
            (pv.backwards_plot_model, pv.is_terminate) = O5zQuiescenceSearchRoutines.search_before_entering_quiescence_node(
                    depth_qs        = depth_qs + depth_qs_extend,
                    pv              = pv,
                    parent_move     = my_move,
                    search_context_model    = search_context_model)

            if pv.is_terminate:
                child_plot_model = pv.backwards_plot_model
            else:
                # NOTE 再帰は廃止。デバッグ作れないから。ここで＜水平線＞。
                child_plot_model = SearchRoutines.create_backwards_plot_model_at_horizon(depth_qs, search_context_model=search_context_model)

            ################
            # MARK: 一手戻す
            ################

            search_context_model.gymnasium.undo_move_o1x()

            ####################
            # MARK: 一手戻した後
            ####################

            depth_qs += 1                 # 深さを１上げる。
            search_context_model.frontwards_plot_model.pop_move()
            search_context_model.gymnasium.health_check_qs_model.pop_node_qs()

            ##################
            # MARK: 手番の処理
            ##################

            (this_branch_value_on_earth, is_update_best) = SearchRoutines.is_update_best(best_pv=best_pv, child_plot_model=child_plot_model, piece_exchange_value_on_earth=piece_exchange_value_on_earth, search_context_model=search_context_model)
                        
            # 最善手の更新（１つに絞る）
            if is_update_best:
                best_pv             = pv
                best_pv.backwards_plot_model    = child_plot_model
                best_move           = my_move
                best_move_cap_pt    = cap_pt
                best_value          = this_branch_value_on_earth

        ########################
        # MARK: 合法手スキャン後
        ########################

        # 指したい手がなかったなら、静止探索の末端局面の後ろだ。
        if best_pv is None:
            return SearchRoutines.create_backwards_plot_model_at_no_candidates(depth_qs=depth_qs, search_context_model=search_context_model)

        # 読み筋に今回の手を付け加える。（ TODO 駒得点も付けたい）
        best_pv.backwards_plot_model.append_move_from_back(
                move                = best_move,
                capture_piece_type  = best_move_cap_pt,
                best_value          = best_value,
                hint                = '')

        return best_pv.backwards_plot_model
