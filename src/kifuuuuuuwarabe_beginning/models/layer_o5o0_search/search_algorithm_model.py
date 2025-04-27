import cshogi

from ..layer_o1o_9o0 import PieceValuesModel
from ..layer_o1o0 import constants, Mars, SquareModel
from ..layer_o2o0 import BackwardsPlotModel
from ..layer_o4o0_rules.negative import DoNotDepromotionModel


class SearchAlgorithmModel:
    """検索アルゴリズム。
    """


    @staticmethod
    def do_move_vertical_all(pv, search_context_model):
        for my_move in pv.vertical_list_of_move_pv:
            search_context_model.gymnasium.do_move_o1x(move = my_move)


    @staticmethod
    def undo_move_vertical_all(pv, search_context_model):
        for i in range(0, len(pv.vertical_list_of_move_pv)):
            search_context_model.gymnasium.undo_move_o1x()


    @staticmethod
    def convert_remaining_moves_to_pv_list(parent_pv, remaining_moves, search_context_model):
        """PVリスト作成。
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

            pv = parent_pv.new_and_append(
                    move_pv     = my_move,
                    cap_pt_pv   = cap_pt,
                    value_pv    = PieceValuesModel.get_piece_exchange_value_on_earth(
                                        pt          = cap_pt,
                                        is_mars     = search_context_model.gymnasium.is_mars),
                    replace_backwards_plot_model    = parent_pv.backwards_plot_model,
                    replace_is_terminate            = False)
            pv_list.append(pv)
        
            # FIXME 読み筋に格納するのは、指した後であるべきでは？
            search_context_model.frontwards_plot_model.append_move_from_front(
                    move    = my_move,
                    cap_pt  = cap_pt)

        return pv_list


    @staticmethod
    def is_update_best(best_pv, child_plot_model, piece_exchange_value_on_earth, search_context_model):
        """ベストを更新するか？

        Returns
        -------
        this_branch_value_on_earth : int
            駒得点。
        is_update_best : bool
            ベストを更新するか。
        """
        # この枝の点（将来の点＋取った駒の点）
        this_branch_value_on_earth = child_plot_model.get_exchange_value_on_earth() + piece_exchange_value_on_earth

        # この枝が長兄なら。
        if best_pv is None:
            old_sibling_value = 0
        else:
            # 兄枝のベスト評価値
            old_sibling_value = best_pv.backwards_plot_model.get_exchange_value_on_earth()     # とりあえず最善の読み筋の点数。

        (a, b) = search_context_model.gymnasium.ptolemaic_theory_model.swap(old_sibling_value, this_branch_value_on_earth)
        # TODO この比較、合っているか？
        return this_branch_value_on_earth, (a < b)
        #return this_branch_value_on_earth, (a > b)


    @staticmethod
    def create_backwards_plot_model_at_game_over(search_context_model):
        search_context_model.gymnasium.health_check_qs_model.on_out_of_termination('＜GameOver＞')
        return BackwardsPlotModel(
                is_mars_at_out_of_termination   = search_context_model.gymnasium.is_mars,
                is_gote_at_out_of_termination   = search_context_model.gymnasium.table.is_gote,
                out_of_termination              = constants.out_of_termination.RESIGN,
                hint_list                       = [],
                move_list                       = [],
                cap_list                        = [],
                list_of_accumulate_exchange_value_on_earth  = [])


    @staticmethod
    def create_backwards_plot_model_at_mate_move_in_1_ply(mate_move, search_context_model):
        search_context_model.gymnasium.health_check_qs_model.append_edge_qs(move=mate_move, hint='＜一手詰め＞')
        search_context_model.gymnasium.health_check_qs_model.on_out_of_termination('＜GameOver＞')
        dst_sq_obj = SquareModel(cshogi.move_to(mate_move))           # ［移動先マス］
        cap_pt = search_context_model.gymnasium.table.piece_type(dst_sq_obj.sq)    # 取った駒種類 NOTE 移動する前に、移動先の駒を取得すること。

        is_mars_at_out_of_termination = not search_context_model.gymnasium.is_mars    # ［詰む］のは、もう１手先だから not する。

        best_plot_model = BackwardsPlotModel(
                is_mars_at_out_of_termination   = is_mars_at_out_of_termination,     
                is_gote_at_out_of_termination   = search_context_model.gymnasium.table.is_gote,
                out_of_termination              = constants.out_of_termination.RESIGN,
                hint_list                       = [],
                move_list                       = [],
                cap_list                        = [],
                list_of_accumulate_exchange_value_on_earth  = [])
    
        # 今回の手を付け加える。
        if is_mars_at_out_of_termination:
            best_value = constants.value.BIG_VALUE        # 火星の負け
        else:
            best_value = constants.value.SMALL_VALUE      # 地球の負け

        best_plot_model.append_move_from_back(
                move                = mate_move,
                capture_piece_type  = cap_pt,
                best_value          = best_value,
                hint                = f"{Mars.japanese(is_mars_at_out_of_termination)}は一手詰まされ")
        return best_plot_model


    @staticmethod
    def create_backwards_plot_model_at_nyugyoku_win(search_context_model):
        search_context_model.gymnasium.health_check_qs_model.on_out_of_termination('＜入玉宣言勝ち＞')
        return BackwardsPlotModel(
                is_mars_at_out_of_termination   = search_context_model.gymnasium.is_mars,
                is_gote_at_out_of_termination   = search_context_model.gymnasium.table.is_gote,
                out_of_termination              = constants.out_of_termination.NYUGYOKU_WIN,
                hint_list                       = [],
                move_list                       = [],
                cap_list                        = [],
                list_of_accumulate_exchange_value_on_earth  = [])


    @staticmethod
    def create_backwards_plot_model_at_horizon(depth_qs, search_context_model):
        search_context_model.gymnasium.health_check_qs_model.on_out_of_termination(f"＜水平線[深QS={depth_qs}]＞")
        return BackwardsPlotModel(
                is_mars_at_out_of_termination   = search_context_model.gymnasium.is_mars,
                is_gote_at_out_of_termination   = search_context_model.gymnasium.table.is_gote,
                out_of_termination              = constants.out_of_termination.MAX_DEPTH_BY_THINK,
                hint_list                       = [],
                move_list                       = [],
                cap_list                        = [],
                list_of_accumulate_exchange_value_on_earth  = [])


    @staticmethod
    def create_backwards_plot_model_at_quiescence(depth_qs, search_context_model):
        search_context_model.gymnasium.health_check_qs_model.on_out_of_termination(f"＜静止[深QS={depth_qs}]＞")
        return BackwardsPlotModel(
                is_mars_at_out_of_termination   = search_context_model.gymnasium.is_mars,
                is_gote_at_out_of_termination   = search_context_model.gymnasium.table.is_gote,
                out_of_termination              = constants.out_of_termination.QUIESCENCE,
                hint_list                       = [],
                move_list                       = [],
                cap_list                        = [],
                list_of_accumulate_exchange_value_on_earth  = [])


    @staticmethod
    def create_backwards_plot_model_at_no_candidates(depth_qs, search_context_model):
        search_context_model.gymnasium.health_check_qs_model.on_out_of_termination(f"＜候補手無し[深QS={depth_qs}]＞")
        return BackwardsPlotModel(
                is_mars_at_out_of_termination   = search_context_model.gymnasium.is_mars,
                is_gote_at_out_of_termination   = search_context_model.gymnasium.table.is_gote,
                out_of_termination              = constants.out_of_termination.NO_CANDIDATES,
                hint_list                       = [],
                move_list                       = [],
                cap_list                        = [],
                list_of_accumulate_exchange_value_on_earth  = [])


    def __init__(self, search_context_model):
        """
        Parameters
        ----------
        search_context_model : SearchContextModel
            探索モデル。
        """
        self._search_context_model = search_context_model


    @property
    def search_context_model(self):
        return self._search_context_model


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
