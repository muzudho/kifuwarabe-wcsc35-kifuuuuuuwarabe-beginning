import cshogi
import time

from ...models.layer_o1o_9o0 import PieceValuesModel
from ...models.layer_o1o0o_9o0_table_helper import TableHelper
from ...models.layer_o1o0 import constants, Mars, SquareModel
from ...models.layer_o4o0_rules.negative import DoNotDepromotionModel


class SearchRoutines:
    """検索アルゴリズム。
    """


    @staticmethod
    def do_move_vertical_all(pv, search_context_model):
        for my_move in pv._leaf_node._get_depth_tn():
            search_context_model.gymnasium.do_move_o1x(move = my_move)


    @staticmethod
    def undo_move_vertical_all(pv, search_context_model):
        for i in range(0, len(pv._leaf_node._get_depth_tn())):
            search_context_model.gymnasium.undo_move_o1x()


    @staticmethod
    def convert_remaining_moves_to_pv_list(parent_pv, remaining_moves, search_context_model):
        """［水平指し手一覧］を［PV一覧］へ変換。
        """
        pv_list = []

        # 残った指し手について
        for my_move in remaining_moves:
            ##################
            # MARK: 一手指す前
            ##################

            # （あれば）駒を取る。
            dst_sq_obj  = SquareModel(cshogi.move_to(my_move))      # ［移動先マス］
            cap_pt      = search_context_model.gymnasium.table.piece_type(dst_sq_obj.sq)    # ［移動先マス］にある［駒種類］。つまりそれは取った駒。打の［移動先マス］は常に空きマス。

            (pv, child_node) = parent_pv.grow_branch_pv(
                    move_arg                    = my_move,
                    cap_pt_arg                  = cap_pt,
                    value_arg                   = PieceValuesModel.get_piece_exchange_value_on_earth(
                                                        pt          = cap_pt,
                                                        is_mars     = search_context_model.gymnasium.is_mars),
                    backwards_plot_model_arg    = parent_pv.deprecated_rooter_backwards_plot_model_in_backward_pv,     # TODO 廃止方針
                    frontward_comment_arg       = '')
            pv_list.append(pv)
        
        return pv_list


    # @staticmethod
    # def is_update_best_search(best_pv, child_pv, piece_exchange_value_on_earth, search_context_model):
    #     """ベストを更新するか？

    #     Returns
    #     -------
    #     this_branch_value_on_earth : int
    #         駒得点。
    #     i s_update_best : bool
    #         ベストを更新するか。
    #     """
    #     # この枝の点（将来の点＋取った駒の点）
    #     this_branch_value_on_earth = child_pv.get_root_value_in_backward_pv() + piece_exchange_value_on_earth

    #     # この枝が長兄なら。
    #     if best_pv is None:
    #         old_sibling_value = 0
    #     else:
    #         # 兄枝のベスト評価値
    #         old_sibling_value = best_pv.get_root_value_in_backward_pv()     # とりあえず最善の読み筋の点数。

    #     (a, b) = search_context_model.gymnasium.ptolemaic_theory_model.swap(old_sibling_value, this_branch_value_on_earth)
    #     # TODO この比較、合っているか？
    #     return this_branch_value_on_earth, (a < b)
    #     #return this_branch_value_on_earth, (a > b)


    @staticmethod
    def remove_drop_moves(remaining_moves):
        """［打］は除外。
        """
        for my_move in reversed(remaining_moves):   # 指し手を全部調べる。
            if cshogi.move_is_drop(my_move):
                remaining_moves.remove(my_move)

        return remaining_moves


    @staticmethod
    def remove_depromoted_moves(remaining_moves, search_context_model):
        """［成れるのに成らない手］は除外。
        """

        do_not_depromotion_model = DoNotDepromotionModel(                                               # 号令［成らないということをするな］を利用。
                basketball_court_model=search_context_model.gymnasium.basketball_court_model)

        do_not_depromotion_model._on_node_entry_negative(               # ノード来訪時。
                remaining_moves = remaining_moves,
                table           = search_context_model.gymnasium.table)

        for my_move in reversed(remaining_moves):   # 指し手を全部調べる。
            # ［成れるのに成らない手］は除外
            mind = do_not_depromotion_model._on_node_exit_negative(
                    move    = my_move,
                    table   = search_context_model.gymnasium.table)
            if mind == constants.mind.WILL_NOT:
                remaining_moves.remove(my_move)

        return remaining_moves


    @staticmethod
    def filtering_capture_or_mate(remaining_moves, rollback_if_empty, search_context_model):
        """駒を取る手と、王手のみ残す。

        Returns
        -------
        remaining_moves : list
            残りの指し手。
        rolled_back : bool
            ロールバックされた。
        """

        rolled_back = False

        if rollback_if_empty:
            old_remaining_moves = remaining_moves.copy()    # バックアップ

        for my_move in reversed(remaining_moves):
            dst_sq_obj  = SquareModel(cshogi.move_to(my_move))      # ［移動先マス］
            cap_pt      = search_context_model.gymnasium.table.piece_type(dst_sq_obj.sq)    # 取った駒種類 NOTE 移動する前に、移動先の駒を取得すること。
            is_capture  = (cap_pt != cshogi.NONE)

            # ２階以降の呼出時は、駒を取る手でなければ無視。
            if not is_capture:
                # ＜📚原則２＞ 王手は（駒を取らない手であっても）探索を続け、深さを１手延長する。
                if search_context_model.gymnasium.table.is_check():
                    #depth_extend += 1  # FIXME 探索が終わらないくなる。
                    pass

                else:
                    remaining_moves.remove(my_move)
                    continue

        if rollback_if_empty and len(remaining_moves) == 0:
            remaining_moves = old_remaining_moves   # 復元
            rolled_back     = True

        return remaining_moves, rolled_back


    @staticmethod
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


    @staticmethod
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


    @staticmethod
    def update_parent_pv_look_in_0_moves(info_depth, parent_pv, search_context_model):
        """ノードに入る前に。

        Returns
        -------
        d eprecated_rooter_backwards_plot_model_pv : B ackwardsPlotModel
            読み筋。
            TODO 廃止方針。
        i s_terminate_pv : bool
            読み終わり。
        """

        ########################
        # MARK: 指す前にやること
        ########################

        cur_time = time.time()                                          # 現在の時間
        erapsed_seconds = cur_time - search_context_model.restart_time    # 経過秒
        if 4 <= erapsed_seconds:                                        # 4秒以上経過してたら、情報出力
            # ［ルート探索］、［カウンター探索］の２を足している。
            print(f"info depth {info_depth} seldepth 0 time 1 nodes {search_context_model.number_of_visited_nodes} score cp 0 string thinking")
            search_context_model.restart_time = cur_time                   # 前回の計測時間を更新

        # 指さなくても分かること（ライブラリー使用）

        # ［終端外］判定。
        if search_context_model.gymnasium.table.is_game_over():
            """手番の投了局面時。
            """
            parent_pv.setup_to_game_over(search_context_model=search_context_model)
            return

        # 一手詰めを詰める
        if not search_context_model.gymnasium.table.is_check():
            """手番玉に王手がかかっていない時で"""

            if (mate_move := search_context_model.gymnasium.table.mate_move_in_1ply()):
                """一手詰めの指し手があれば、それを取得"""
                dst_sq_obj  = SquareModel(cshogi.move_to(mate_move))      # ［移動先マス］
                cap_pt      = search_context_model.gymnasium.table.piece_type(dst_sq_obj.sq)    # ［移動先マス］にある［駒種類］。つまりそれは取った駒。打の［移動先マス］は常に空きマス。
                value_pt    = PieceValuesModel.get_piece_exchange_value_on_earth(
                                    pt          = cap_pt,
                                    is_mars     = search_context_model.gymnasium.is_mars)
                parent_pv.setup_to_mate_move_in_1_ply(info_depth=info_depth, mate_move=mate_move, search_context_model=search_context_model)
                return

        if search_context_model.gymnasium.table.is_nyugyoku():
            """手番の入玉宣言勝ち局面時。
            """
            parent_pv.setup_to_nyugyoku_win(search_context_model=search_context_model)
            return
